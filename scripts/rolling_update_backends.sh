#!/usr/bin/env bash
set -Eeuo pipefail

COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.yml}"
PROJECT_ROOT="${PROJECT_ROOT:-$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)}"
HEALTH_URL="${HEALTH_URL:-http://127.0.0.1:80/api/health}"
THINK_URL="${THINK_URL:-http://127.0.0.1:80/api/shell/think}"
HEALTH_TIMEOUT_SECONDS="${HEALTH_TIMEOUT_SECONDS:-90}"
POLL_INTERVAL_SECONDS="${POLL_INTERVAL_SECONDS:-2}"
BUILD_FIRST="${BUILD_FIRST:-0}"
SKIP_THINK_SMOKE="${SKIP_THINK_SMOKE:-0}"

if [[ "$COMPOSE_FILE" != /* ]]; then
  COMPOSE_FILE="$PROJECT_ROOT/$COMPOSE_FILE"
fi

wait_http_200() {
  local url="$1"
  local timeout="$2"
  local poll="$3"
  local deadline=$((SECONDS + timeout))

  while (( SECONDS < deadline )); do
    if curl -fsS --max-time 5 "$url" >/dev/null 2>&1; then
      return 0
    fi
    sleep "$poll"
  done

  return 1
}

wait_service_healthy() {
  local service="$1"
  local timeout="$2"
  local poll="$3"
  local deadline=$((SECONDS + timeout))

  while (( SECONDS < deadline )); do
    local container_id
    container_id="$(docker compose -f "$COMPOSE_FILE" ps -q "$service" 2>/dev/null || true)"

    if [[ -n "$container_id" ]]; then
      local status
      status="$(docker inspect --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' "$container_id" 2>/dev/null || echo "starting")"
      if [[ "$status" == "healthy" ]]; then
        return 0
      fi
    fi

    sleep "$poll"
  done

  return 1
}

invoke_think_smoke() {
  local url="$1"
  local body='{"prompt":"rolling update smoke check","task_type":"reasoning"}'
  local response

  response="$(curl -fsS -X POST -H 'Content-Type: application/json' --data "$body" --max-time 15 "$url")" || return 1

  python3 - "$response" <<'PY'
import json, sys
payload = sys.argv[1]
try:
    data = json.loads(payload)
except json.JSONDecodeError as exc:
    raise SystemExit(f"invalid JSON smoke response: {exc}")
if not isinstance(data, dict) or 'status' not in data:
    raise SystemExit("think smoke response is missing status")
print(f"Think smoke OK (status={data.get('status')}, engine={data.get('engine', 'unknown')})")
PY
}

if [[ ! -f "$COMPOSE_FILE" ]]; then
  echo "docker-compose.yml not found: $COMPOSE_FILE" >&2
  exit 1
fi

printf '%s\n' "========================================"
printf '%s\n' "  NEUROSONIC ROLLING UPDATE"
printf '%s\n' "========================================"
printf 'Compose: %s\n' "$COMPOSE_FILE"
printf 'Root:    %s\n' "$PROJECT_ROOT"
printf '\n'

cd "$PROJECT_ROOT"

if [[ "$BUILD_FIRST" == "1" ]]; then
  echo "[0/4] Building backend images..."
  docker compose -f "$COMPOSE_FILE" build backend backend_b
fi

echo "[1/4] Ensuring service topology is up..."
docker compose -f "$COMPOSE_FILE" up -d --no-deps backend backend_b web

if ! wait_http_200 "$HEALTH_URL" "$HEALTH_TIMEOUT_SECONDS" "$POLL_INTERVAL_SECONDS"; then
  echo "API health did not become 200 in time: $HEALTH_URL" >&2
  exit 1
fi

echo "  ✅ Initial health OK"

step=2
for service in backend backend_b; do
  echo "[$step/4] Recreating $service ..."
  docker compose -f "$COMPOSE_FILE" up -d --force-recreate --no-deps "$service"

  if ! wait_service_healthy "$service" "$HEALTH_TIMEOUT_SECONDS" "$POLL_INTERVAL_SECONDS"; then
    echo "Service $service did not become healthy." >&2
    exit 1
  fi

  if ! wait_http_200 "$HEALTH_URL" "$HEALTH_TIMEOUT_SECONDS" "$POLL_INTERVAL_SECONDS"; then
    echo "API health failed after recreate of $service" >&2
    exit 1
  fi

  if [[ "$SKIP_THINK_SMOKE" != "1" ]]; then
    invoke_think_smoke "$THINK_URL"
    echo "  ✅ Think smoke OK on $service"
  else
    echo "  ✅ Health OK on $service (smoke skipped)"
  fi

  step=$((step + 1))
done

echo "[4/4] Final service status:"
docker compose -f "$COMPOSE_FILE" ps

echo

echo "✅ Rolling update completed successfully."
