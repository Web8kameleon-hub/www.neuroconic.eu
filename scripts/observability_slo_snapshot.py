#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate SLO snapshot and error-budget status.")
    parser.add_argument(
        "--availability",
        default="docs/production/evidence/availability_trend.json",
        help="Availability trend JSON path.",
    )
    parser.add_argument(
        "--latency",
        default="docs/production/evidence/latency_trend.json",
        help="Latency trend JSON path.",
    )
    parser.add_argument(
        "--output-json",
        default="docs/production/evidence/slo_snapshot_latest.json",
        help="Output SLO snapshot JSON.",
    )
    parser.add_argument(
        "--output-md",
        default="docs/production/evidence/error_budget_status_latest.md",
        help="Output error budget markdown summary.",
    )
    parser.add_argument("--availability-target", type=float, default=99.5)
    parser.add_argument("--latency-p95-target", type=float, default=450.0)
    parser.add_argument("--pretty", action="store_true")
    return parser.parse_args()


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _latest(series: list[dict[str, Any]]) -> dict[str, Any]:
    if not series:
        return {}
    return series[-1]


def _error_budget_burn(observed_availability_percent: float, target_percent: float) -> float:
    budget = max(0.000001, 100.0 - target_percent)
    consumed = max(0.0, target_percent - observed_availability_percent)
    return round(consumed / budget, 4)


def _status_from_burn(burn_rate: float) -> str:
    if burn_rate > 1.0:
        return "critical"
    if burn_rate >= 0.5:
        return "warning"
    return "healthy"


def main() -> int:
    args = _parse_args()

    availability_data = _load(Path(args.availability))
    latency_data = _load(Path(args.latency))

    availability_latest = _latest(availability_data.get("series", []))
    latency_latest = _latest(latency_data.get("series", []))

    observed_availability = float(availability_latest.get("availability_percent", 0.0))
    observed_p95 = float(latency_latest.get("avg_p95_ms", 0.0))
    burn_rate = _error_budget_burn(observed_availability, args.availability_target)
    status = _status_from_burn(burn_rate)

    payload = {
        "generated_at": time.time(),
        "targets": {
            "availability_percent": args.availability_target,
            "latency_p95_ms": args.latency_p95_target,
        },
        "observed": {
            "availability_percent": round(observed_availability, 3),
            "latency_p95_ms": round(observed_p95, 3),
            "availability_source": availability_latest.get("source"),
            "latency_source": latency_latest.get("source"),
        },
        "error_budget": {
            "burn_rate": burn_rate,
            "status": status,
        },
        "slo_eval": {
            "availability_met": observed_availability >= args.availability_target,
            "latency_p95_met": observed_p95 <= args.latency_p95_target,
        },
    }

    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    output_json.parent.mkdir(parents=True, exist_ok=True)

    output_json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None),
        encoding="utf-8",
    )

    summary = "\n".join(
        [
            "# Error Budget Status (Latest)",
            "",
            f"- Availability target: `{args.availability_target}%`",
            f"- Observed availability: `{observed_availability}%`",
            f"- P95 target: `{args.latency_p95_target} ms`",
            f"- Observed P95: `{observed_p95} ms`",
            f"- Burn rate: `{burn_rate}`",
            f"- Status: `{status}`",
        ]
    )
    output_md.write_text(summary + "\n", encoding="utf-8")

    print(f"SLO snapshot written: {output_json}")
    print(f"Error budget summary written: {output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
