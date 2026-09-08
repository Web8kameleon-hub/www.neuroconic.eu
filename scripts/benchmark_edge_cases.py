#!/usr/bin/env python3
"""Run automated edge-case benchmarks against a live Neurosonic backend.

This script focuses only on edge scenarios and does not produce mocked output.
"""

from __future__ import annotations

import argparse
import json
import statistics
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


@dataclass(frozen=True)
class EdgeScenario:
    name: str
    endpoint: str
    method: str
    payload: dict[str, Any] | None
    verifier: Callable[[int, dict[str, Any]], bool]


def _percentile(values: list[float], quantile: float) -> float:
    if len(values) == 1:
        return values[0]
    index = (len(values) - 1) * quantile
    lower = int(index)
    upper = min(lower + 1, len(values) - 1)
    return values[lower] * (1.0 - index + lower) + values[upper] * (index - lower)


def _has_trace_contract(status: int, body: dict[str, Any]) -> bool:
    trace = body.get("trace")
    verification = body.get("verification")
    return (
        200 <= status < 300
        and isinstance(trace, dict)
        and isinstance(verification, dict)
        and isinstance(trace.get("pipeline"), list)
        and "reasoning_validated" in verification
    )


def _prompt_empty_error(status: int, body: dict[str, Any]) -> bool:
    return (
        200 <= status < 300
        and body.get("success") is False
        and body.get("error") == "Prompt is empty"
    )


def _requires_liability_ack(status: int, body: dict[str, Any]) -> bool:
    return (
        200 <= status < 300
        and body.get("success") is False
        and body.get("error") == "liability_ack must be true"
    )


def _rejects_private_address(status: int, body: dict[str, Any]) -> bool:
    return (
        200 <= status < 300
        and body.get("success") is False
        and "private or local network" in str(body.get("error", ""))
    )


def _rejects_sensitive_metadata(status: int, body: dict[str, Any]) -> bool:
    return (
        200 <= status < 300
        and body.get("success") is False
        and "sensitive key" in str(body.get("error", ""))
    )


def _scenarios(long_prompt_size: int) -> list[EdgeScenario]:
    return [
        EdgeScenario(
            name="shell_empty_prompt_edge",
            endpoint="/api/shell/think",
            method="POST",
            payload={"prompt": "", "task_type": "reasoning"},
            verifier=_prompt_empty_error,
        ),
        EdgeScenario(
            name="shell_whitespace_prompt_edge",
            endpoint="/api/shell/think",
            method="POST",
            payload={"prompt": "  \n\t ", "task_type": "reasoning"},
            verifier=_prompt_empty_error,
        ),
        EdgeScenario(
            name="shell_long_prompt_edge",
            endpoint="/api/shell/think",
            method="POST",
            payload={"prompt": "A" * long_prompt_size, "task_type": "reasoning"},
            verifier=_has_trace_contract,
        ),
        EdgeScenario(
            name="plugin_attach_missing_liability_ack_edge",
            endpoint="/api/ui/plugins/edge-bench-profile",
            method="POST",
            payload={"address": "https://plugins.example.com/connector"},
            verifier=_requires_liability_ack,
        ),
        EdgeScenario(
            name="plugin_attach_private_network_edge",
            endpoint="/api/ui/plugins/edge-bench-profile",
            method="POST",
            payload={"address": "http://127.0.0.1:8080", "liability_ack": True},
            verifier=_rejects_private_address,
        ),
        EdgeScenario(
            name="plugin_attach_sensitive_metadata_edge",
            endpoint="/api/ui/plugins/edge-bench-profile",
            method="POST",
            payload={
                "address": "https://plugins.example.com/connector",
                "liability_ack": True,
                "metadata": {"api_key": "redacted"},
            },
            verifier=_rejects_sensitive_metadata,
        ),
    ]


def _request(
    base_url: str,
    scenario: EdgeScenario,
    timeout: float,
) -> tuple[int, dict[str, Any]]:
    data = json.dumps(scenario.payload).encode("utf-8") if scenario.payload is not None else None
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}{scenario.endpoint}",
        data=data,
        method=scenario.method,
        headers={"Content-Type": "application/json"} if data is not None else {},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = response.status
            raw = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as error:
        status = error.code
        raw = error.read().decode("utf-8", errors="replace")

    body = json.loads(raw)
    if not isinstance(body, dict):
        raise ValueError(
            f"{scenario.name}: server returned a non-object JSON response"
        )
    return status, body


def _run_scenario(
    base_url: str,
    scenario: EdgeScenario,
    iterations: int,
    warmup: int,
    timeout: float,
) -> dict[str, Any]:
    latencies: list[float] = []
    passed = 0
    samples: list[dict[str, Any]] = []

    for index in range(iterations + warmup):
        started = time.perf_counter()
        status, body = _request(base_url, scenario, timeout)
        elapsed_ms = (time.perf_counter() - started) * 1000

        if index < warmup:
            continue

        latencies.append(elapsed_ms)
        is_pass = scenario.verifier(status, body)
        passed += int(is_pass)
        if len(samples) < 3:
            samples.append(
                {
                    "status_code": status,
                    "pass": is_pass,
                    "success": body.get("success"),
                    "status": body.get("status"),
                    "error": body.get("error"),
                }
            )

    ordered = sorted(latencies)
    total_seconds = sum(latencies) / 1000
    return {
        "name": scenario.name,
        "endpoint": scenario.endpoint,
        "iterations": iterations,
        "warmup": warmup,
        "pass_rate": round(passed / iterations, 4),
        "throughput_rps": round(len(latencies) / total_seconds, 3)
        if total_seconds
        else 0.0,
        "latency_ms": {
            "min": round(ordered[0], 3),
            "p50": round(_percentile(ordered, 0.50), 3),
            "p95": round(_percentile(ordered, 0.95), 3),
            "max": round(ordered[-1], 3),
            "mean": round(statistics.mean(latencies), 3),
            "stdev": round(statistics.pstdev(latencies), 3)
            if len(latencies) > 1
            else 0.0,
        },
        "samples": samples,
    }


def _to_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Edge Case Benchmark Report",
        "",
        f"- Base URL: `{report['base_url']}`",
        f"- Iterations: `{report['iterations']}`",
        f"- Warmup: `{report['warmup']}`",
        f"- Overall pass rate: `{report['totals']['overall_pass_rate']}`",
        "",
        "| Scenario | Pass Rate | P95 (ms) | Throughput (rps) |",
        "| --- | ---: | ---: | ---: |",
    ]
    for item in report["results"]:
        lines.append(
            "| "
            f"{item['name']} | "
            f"{item['pass_rate']} | "
            f"{item['latency_ms']['p95']} | "
            f"{item['throughput_rps']} |"
        )
    lines.append("")
    return "\n".join(lines)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run automated edge-case benchmark scenarios."
    )
    parser.add_argument(
        "--base-url",
        required=True,
        help="Running backend URL, e.g. http://127.0.0.1:8000",
    )
    parser.add_argument("--iterations", type=int, default=12)
    parser.add_argument("--warmup", type=int, default=2)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--long-prompt-size", type=int, default=8192)
    parser.add_argument(
        "--output-json",
        default="",
        help="Optional JSON output path; defaults to logs/benchmarks/live-edge-benchmark-*.json",
    )
    parser.add_argument(
        "--output-md",
        default="docs/production/evidence/edge_benchmark_latest.md",
        help="Markdown summary output path.",
    )
    parser.add_argument("--pretty", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    if (
        args.iterations <= 0
        or args.warmup < 0
        or args.timeout <= 0
        or args.long_prompt_size < 16
    ):
        raise ValueError(
            "iterations > 0, warmup >= 0, timeout > 0, "
            "and long-prompt-size >= 16 are required"
        )

    scenarios = _scenarios(args.long_prompt_size)
    created_at = time.time()
    results = [
        _run_scenario(
            args.base_url,
            scenario,
            iterations=args.iterations,
            warmup=args.warmup,
            timeout=args.timeout,
        )
        for scenario in scenarios
    ]
    overall_pass_rate = round(
        statistics.mean(item["pass_rate"] for item in results),
        4,
    )

    report = {
        "benchmark": "neurosonic-edge-case-benchmark",
        "created_at": created_at,
        "base_url": args.base_url,
        "iterations": args.iterations,
        "warmup": args.warmup,
        "long_prompt_size": args.long_prompt_size,
        "totals": {
            "scenario_count": len(results),
            "overall_pass_rate": overall_pass_rate,
        },
        "results": results,
    }

    output_json_path = (
        Path(args.output_json)
        if args.output_json
        else Path(
            "logs/benchmarks/live-edge-benchmark-"
            + time.strftime("%Y%m%d-%H%M%S")
            + ".json"
        )
    )
    output_md_path = Path(args.output_md)

    output_json_path.parent.mkdir(parents=True, exist_ok=True)
    output_md_path.parent.mkdir(parents=True, exist_ok=True)

    output_json_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2 if args.pretty else None)
        + "\n",
        encoding="utf-8",
    )
    output_md_path.write_text(_to_markdown(report), encoding="utf-8")

    print(f"Edge benchmark completed: {output_json_path}")
    print(f"Markdown summary: {output_md_path}")
    print(
        f"Overall edge-case pass rate: {overall_pass_rate:.2%} | "
        f"Scenarios: {len(results)}"
    )
    return 0 if overall_pass_rate == 1.0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
