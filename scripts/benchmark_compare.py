#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare two benchmark outputs and publish evidence artifacts."
    )
    parser.add_argument("--baseline", default=None, help="Path to baseline benchmark JSON.")
    parser.add_argument("--candidate", default=None, help="Path to candidate benchmark JSON.")
    parser.add_argument(
        "--benchmarks-dir",
        default="logs/benchmarks",
        help="Directory used when baseline/candidate are not explicitly set.",
    )
    parser.add_argument(
        "--output-json",
        default="docs/production/evidence/benchmark_compare_latest.json",
        help="Output JSON report path.",
    )
    parser.add_argument(
        "--output-md",
        default="docs/production/evidence/benchmark_compare_latest.md",
        help="Output Markdown report path.",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty print JSON output.")
    return parser.parse_args()


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _pick_latest_two(benchmarks_dir: Path) -> tuple[Path, Path]:
    files = sorted(
        benchmarks_dir.glob("live-benchmark-*.json"), key=lambda item: item.stat().st_mtime
    )
    if len(files) < 2:
        raise ValueError("Need at least two live benchmark files in logs/benchmarks to compare.")
    return files[-2], files[-1]


def _scenario_map(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for item in data.get("results", []):
        name = str(item.get("name", ""))
        if name:
            output[name] = item
    return output


def _delta(candidate: float, baseline: float) -> float:
    return round(candidate - baseline, 3)


def _delta_percent(candidate: float, baseline: float) -> float:
    if baseline == 0:
        return 0.0
    return round(((candidate - baseline) / baseline) * 100.0, 2)


def _compare(baseline: dict[str, Any], candidate: dict[str, Any], baseline_path: Path, candidate_path: Path) -> dict[str, Any]:
    base_scenarios = _scenario_map(baseline)
    cand_scenarios = _scenario_map(candidate)

    names = sorted(set(base_scenarios.keys()) & set(cand_scenarios.keys()))
    rows: list[dict[str, Any]] = []

    for name in names:
        base = base_scenarios[name]
        cand = cand_scenarios[name]

        base_p95 = _safe_float(base.get("latency_ms", {}).get("p95"))
        cand_p95 = _safe_float(cand.get("latency_ms", {}).get("p95"))
        base_p50 = _safe_float(base.get("latency_ms", {}).get("p50"))
        cand_p50 = _safe_float(cand.get("latency_ms", {}).get("p50"))
        base_rps = _safe_float(base.get("throughput_rps"))
        cand_rps = _safe_float(cand.get("throughput_rps"))
        base_pass = _safe_float(base.get("pass_rate"))
        cand_pass = _safe_float(cand.get("pass_rate"))

        rows.append(
            {
                "scenario": name,
                "baseline": {
                    "p50_ms": base_p50,
                    "p95_ms": base_p95,
                    "throughput_rps": base_rps,
                    "pass_rate": base_pass,
                },
                "candidate": {
                    "p50_ms": cand_p50,
                    "p95_ms": cand_p95,
                    "throughput_rps": cand_rps,
                    "pass_rate": cand_pass,
                },
                "delta": {
                    "p50_ms": _delta(cand_p50, base_p50),
                    "p95_ms": _delta(cand_p95, base_p95),
                    "throughput_rps": _delta(cand_rps, base_rps),
                    "pass_rate": round(cand_pass - base_pass, 4),
                    "p95_percent": _delta_percent(cand_p95, base_p95),
                    "throughput_percent": _delta_percent(cand_rps, base_rps),
                },
            }
        )

    base_overall = _safe_float(baseline.get("totals", {}).get("overall_pass_rate"))
    cand_overall = _safe_float(candidate.get("totals", {}).get("overall_pass_rate"))

    return {
        "benchmark": "neurosonic-comparative-evidence",
        "created_at": time.time(),
        "baseline_file": str(baseline_path).replace("\\", "/"),
        "candidate_file": str(candidate_path).replace("\\", "/"),
        "baseline_profile": baseline.get("profile", {}).get("name", "unknown"),
        "candidate_profile": candidate.get("profile", {}).get("name", "unknown"),
        "totals": {
            "shared_scenarios": len(rows),
            "baseline_overall_pass_rate": round(base_overall, 4),
            "candidate_overall_pass_rate": round(cand_overall, 4),
            "overall_pass_rate_delta": round(cand_overall - base_overall, 4),
        },
        "scenarios": rows,
    }


def _to_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Comparative Benchmark Evidence",
        "",
        f"- Baseline: `{report['baseline_file']}`",
        f"- Candidate: `{report['candidate_file']}`",
        f"- Shared scenarios: `{report['totals']['shared_scenarios']}`",
        f"- Overall pass-rate delta: `{report['totals']['overall_pass_rate_delta']}`",
        "",
        "| Scenario | Δ p95 (ms) | Δ p95 (%) | Δ Throughput (rps) | Δ Throughput (%) | Δ Pass Rate |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]

    for row in report.get("scenarios", []):
        delta = row["delta"]
        lines.append(
            "| "
            f"{row['scenario']} | "
            f"{delta['p95_ms']} | "
            f"{delta['p95_percent']} | "
            f"{delta['throughput_rps']} | "
            f"{delta['throughput_percent']} | "
            f"{delta['pass_rate']} |"
        )

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = _parse_args()

    if args.baseline and args.candidate:
        baseline_path = Path(args.baseline)
        candidate_path = Path(args.candidate)
    else:
        baseline_path, candidate_path = _pick_latest_two(Path(args.benchmarks_dir))

    baseline_data = _load_json(baseline_path)
    candidate_data = _load_json(candidate_path)

    report = _compare(baseline_data, candidate_data, baseline_path, candidate_path)

    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    output_json.parent.mkdir(parents=True, exist_ok=True)

    output_json.write_text(
        json.dumps(report, ensure_ascii=False, indent=2 if args.pretty else None),
        encoding="utf-8",
    )
    output_md.write_text(_to_markdown(report), encoding="utf-8")

    print(f"Comparative evidence written: {output_json}")
    print(f"Markdown summary written: {output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
