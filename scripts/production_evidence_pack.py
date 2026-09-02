#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

BENCHMARK_GLOB = "first-benchmark-*.json"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate production evidence artifacts from benchmark history."
    )
    parser.add_argument(
        "--benchmarks-dir",
        default="logs/benchmarks",
        help="Directory containing first benchmark JSON files.",
    )
    parser.add_argument(
        "--evidence-dir",
        default="docs/production/evidence",
        help="Directory where evidence artifacts are written.",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty print JSON outputs.")
    return parser.parse_args()


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _load_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _read_benchmark_points(benchmarks_dir: Path) -> list[dict[str, Any]]:
    points: list[dict[str, Any]] = []

    for path in sorted(benchmarks_dir.glob(BENCHMARK_GLOB)):
        data = _load_json(path)
        if not data:
            continue

        created_at = _safe_float(data.get("created_at"), 0.0)
        if created_at <= 0:
            created_at = path.stat().st_mtime

        results = data.get("results", [])
        p50_values = [_safe_float(item.get("latency_ms", {}).get("p50")) for item in results]
        p95_values = [_safe_float(item.get("latency_ms", {}).get("p95")) for item in results]

        p50_values = [item for item in p50_values if item > 0]
        p95_values = [item for item in p95_values if item > 0]

        avg_p50 = sum(p50_values) / len(p50_values) if p50_values else 0.0
        avg_p95 = sum(p95_values) / len(p95_values) if p95_values else 0.0

        pass_rate = _safe_float(data.get("totals", {}).get("overall_pass_rate"), 0.0)

        points.append(
            {
                "timestamp": created_at,
                "date_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(created_at)),
                "file": str(path).replace("\\", "/"),
                "profile": data.get("profile", {}).get("name", "unknown"),
                "scenario_count": len(results),
                "overall_pass_rate": round(pass_rate, 4),
                "availability_percent": round(pass_rate * 100.0, 2),
                "avg_p50_ms": round(avg_p50, 3),
                "avg_p95_ms": round(avg_p95, 3),
            }
        )

    points.sort(key=lambda item: item["timestamp"])
    return points


def _build_latency_trend(points: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "metric": "latency",
        "unit": "ms",
        "series": [
            {
                "date_utc": item["date_utc"],
                "profile": item["profile"],
                "avg_p50_ms": item["avg_p50_ms"],
                "avg_p95_ms": item["avg_p95_ms"],
                "source": item["file"],
            }
            for item in points
        ],
    }


def _build_availability_trend(points: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "metric": "availability",
        "unit": "percent",
        "definition": "Derived from benchmark overall_pass_rate for tracked scenarios.",
        "series": [
            {
                "date_utc": item["date_utc"],
                "profile": item["profile"],
                "availability_percent": item["availability_percent"],
                "overall_pass_rate": item["overall_pass_rate"],
                "source": item["file"],
            }
            for item in points
        ],
    }


def _write_json(path: Path, payload: dict[str, Any], pretty: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2 if pretty else None),
        encoding="utf-8",
    )


def _ensure_incident_log(path: Path) -> None:
    if path.exists():
        return
    content = """# Incident Log\n\nTrack only real incidents with timestamps, impact, root cause, and corrective actions.\n\n| Date (UTC) | Severity | Summary | Impact | Root Cause | Corrective Action | Status |\n| --- | --- | --- | --- | --- | --- | --- |\n| _pending_ | _n/a_ | No production incident recorded yet | _n/a_ | _n/a_ | _n/a_ | Open |\n"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _ensure_rollback_drills(path: Path) -> None:
    if path.exists():
        return
    content = """# Rollback Drills\n\nTrack controlled rollback exercises for deploy confidence.\n\n| Date (UTC) | Release | Trigger | RTO (min) | Data Loss | Result | Notes |\n| --- | --- | --- | --- | --- | --- | --- |\n| _pending_ | _n/a_ | _n/a_ | _n/a_ | _n/a_ | Not run | Schedule first drill |\n"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    args = _parse_args()
    benchmarks_dir = Path(args.benchmarks_dir)
    evidence_dir = Path(args.evidence_dir)

    points = _read_benchmark_points(benchmarks_dir)

    latency_path = evidence_dir / "latency_trend.json"
    availability_path = evidence_dir / "availability_trend.json"
    incident_log_path = evidence_dir / "incident_log.md"
    rollback_path = evidence_dir / "rollback_drills.md"

    _write_json(latency_path, _build_latency_trend(points), pretty=args.pretty)
    _write_json(availability_path, _build_availability_trend(points), pretty=args.pretty)
    _ensure_incident_log(incident_log_path)
    _ensure_rollback_drills(rollback_path)

    print(f"Evidence pack generated in: {evidence_dir}")
    print(f"Benchmark points processed: {len(points)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
