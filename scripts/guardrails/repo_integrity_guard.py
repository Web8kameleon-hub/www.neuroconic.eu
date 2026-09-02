#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


@dataclass
class CheckFailure:
    code: str
    message: str


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _parse_services(compose_file: Path) -> dict[str, dict[str, bool]]:
    data: dict[str, dict[str, bool]] = {}
    if not compose_file.exists():
        return data

    lines = _read_text(compose_file).splitlines()
    in_services = False
    current_service: str | None = None

    for line in lines:
        if not in_services:
            if re.match(r"^services\s*:\s*$", line):
                in_services = True
            continue

        if not line.strip() or line.strip().startswith("#"):
            continue

        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()

        if indent == 0:
            break

        if indent == 2 and re.match(r"^[A-Za-z0-9_.-]+\s*:\s*$", stripped):
            current_service = stripped.split(":", 1)[0].strip()
            data[current_service] = {"healthcheck": False}
            continue

        if current_service and indent == 4 and stripped.startswith("healthcheck:"):
            data[current_service]["healthcheck"] = True

    return data


def _read_service_list(path: Path) -> list[str]:
    if not path.exists():
        return []
    items = [line.strip() for line in _read_text(path).splitlines()]
    return sorted({x for x in items if x and not x.startswith("#")})


def _has_regex(path: Path, pattern: str) -> bool:
    if not path.exists():
        return False
    return re.search(pattern, _read_text(path), flags=re.MULTILINE | re.IGNORECASE) is not None


def main() -> int:
    failures: list[CheckFailure] = []

    compose_file = ROOT / "docker-compose.yml"
    canonical_list_file = ROOT / "scripts" / "guardrails" / "compose.services.txt"

    services = _parse_services(compose_file)
    if not compose_file.exists():
        failures.append(CheckFailure("MISSING_COMPOSE", "Missing docker-compose.yml"))
    if not canonical_list_file.exists():
        failures.append(
            CheckFailure(
                "MISSING_CANONICAL_SERVICE_LIST",
                "Missing scripts/guardrails/compose.services.txt",
            )
        )

    required_services = ["lightning-spp", "backend", "backend_b", "web"]
    for service in required_services:
        if service not in services:
            failures.append(
                CheckFailure(
                    "MISSING_CRITICAL_SERVICE",
                    f"Service '{service}' is missing in docker-compose.yml",
                )
            )

    health_required = ["lightning-spp", "backend", "backend_b", "web"]
    for service in health_required:
        if service in services and not services[service].get("healthcheck", False):
            failures.append(
                CheckFailure(
                    "MISSING_HEALTHCHECK",
                    f"Service '{service}' has no healthcheck in docker-compose.yml",
                )
            )

    if canonical_list_file.exists():
        canonical_services = set(_read_service_list(canonical_list_file))
        current_services = set(services.keys())
        missing_from_compose = sorted(canonical_services - current_services)
        missing_from_canonical = sorted(current_services - canonical_services)
        if missing_from_compose or missing_from_canonical:
            failures.append(
                CheckFailure(
                    "CANONICAL_SERVICE_LIST_MISMATCH",
                    "docker-compose.yml and scripts/guardrails/compose.services.txt are not aligned",
                )
            )

    required_files = [
        ROOT / "backend" / "main.py",
        ROOT / "neurosonic_no_fake_police.py",
        ROOT / "deploy" / "nginx.conf",
        ROOT / "scripts" / "rolling_update_backends.ps1",
    ]
    for required in required_files:
        if not required.exists():
            failures.append(
                CheckFailure("MISSING_CRITICAL_FILE", f"Missing required file: {required.relative_to(ROOT)}")
            )

    endpoint_contracts = [
        (ROOT / "backend" / "main.py", r"@app\.get\(\s*[\"']?/api/health[\"']?"),
        (ROOT / "backend" / "main.py", r"@app\.post\(\s*[\"']?/api/shell/think[\"']?"),
        (ROOT / "backend" / "main.py", r"@app\.post\(\s*[\"']?/api/ui/plugins/\{profile_id\}[\"']?"),
        (ROOT / "backend" / "main.py", r"@app\.post\(\s*[\"']?/api/lightning/pipeline[\"']?"),
    ]

    for file_path, pattern in endpoint_contracts:
        if not _has_regex(file_path, pattern):
            failures.append(
                CheckFailure(
                    "MISSING_ENDPOINT_CONTRACT",
                    f"Missing endpoint contract in {file_path.relative_to(ROOT)} for pattern: {pattern}",
                )
            )

    report = {
        "ok": len(failures) == 0,
        "checked_at": "runtime",
        "compose": str(compose_file.relative_to(ROOT)),
        "service_count": len(services),
        "failures": [failure.__dict__ for failure in failures],
    }

    out = ROOT / "docs" / "production" / "canonical" / "repo_integrity_guard_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=True), encoding="utf-8")

    if failures:
        print("[REPO-INTEGRITY-GUARD] FAIL")
        for failure in failures:
            print(f"- {failure.code}: {failure.message}")
        print(f"Report: {out.relative_to(ROOT)}")
        return 1

    print("[REPO-INTEGRITY-GUARD] PASS")
    print(f"Services checked: {len(services)}")
    print(f"Report: {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())