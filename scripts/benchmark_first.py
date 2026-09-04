#!/usr/bin/env python3
"""Benchmark a running Neurosonic backend through its public HTTP API.

This harness never changes runtime objects and never manufactures endpoint
responses. It records measurements only from the server supplied with
``--base-url``. A backend that is unavailable is a failed benchmark.
"""

from __future__ import annotations

import argparse
import json
import statistics
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable


@dataclass(frozen=True)
class TuningProfile:
    name: str
    iterations: int
    warmup: int
    long_prompt_size: int


@dataclass(frozen=True)
class Scenario:
    name: str
    endpoint: str
    method: str
    payload_factory: Callable[[TuningProfile], dict[str, Any] | None]
    verifier: Callable[[int, dict[str, Any]], bool]


PROFILES = {
    "quick": TuningProfile("quick", iterations=10, warmup=2, long_prompt_size=2048),
    "standard": TuningProfile("standard", iterations=50, warmup=5, long_prompt_size=8192),
    "stress": TuningProfile("stress", iterations=200, warmup=15, long_prompt_size=32768),
}


def _percentile(values: list[float], quantile: float) -> float:
    if len(values) == 1:
        return values[0]
    index = (len(values) - 1) * quantile
    lower = int(index)
    upper = min(lower + 1, len(values) - 1)
    return values[lower] * (1.0 - index + lower) + values[upper] * (index - lower)


def _is_success(status: int, body: dict[str, Any]) -> bool:
    return 200 <= status < 300 and body.get("success") is True


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


def _scenarios() -> list[Scenario]:
    return [
        Scenario("api_health", "/api/health", "GET", lambda _: None, _is_success),
        Scenario(
            "shell_think_empty_prompt_edge",
            "/api/shell/think",
            "POST",
            lambda _: {"prompt": "   ", "task_type": "reasoning"},
            lambda status, body: (
                200 <= status < 300
                and body.get("success") is False
                and body.get("error") == "Prompt is empty"
            ),
        ),
        Scenario(
            "shell_think_contract",
            "/api/shell/think",
            "POST",
            lambda _: {
                "prompt": "Explain the active governance policy.",
                "task_type": "reasoning",
            },
            _has_trace_contract,
        ),
        Scenario(
            "shell_think_long_prompt_edge",
            "/api/shell/think",
            "POST",
            lambda profile: {
                "prompt": "A" * profile.long_prompt_size,
                "task_type": "reasoning",
            },
            _has_trace_contract,
        ),
        Scenario(
            "plugin_attach_private_network_edge",
            "/api/ui/plugins/bench-profile",
            "POST",
            lambda _: {"address": "http://127.0.0.1:8080", "liability_ack": True},
            _rejects_private_address,
        ),
        Scenario(
            "plugin_attach_sensitive_metadata_edge",
            "/api/ui/plugins/bench-profile",
            "POST",
            lambda _: {
                "address": "https://plugins.example.com/connector",
                "liability_ack": True,
                "metadata": {"api_key": "redacted"},
            },
            _rejects_sensitive_metadata,
        ),
    ]


def _request(
    base_url: str,
    scenario: Scenario,
    payload: dict[str, Any] | None,
    timeout: float,
) -> tuple[int, dict[str, Any]]:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
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
        raise ValueError(f"{scenario.name}: server returned a non-object JSON response")
    return status, body


def _run_scenario(
    base_url: str, scenario: Scenario, profile: TuningProfile, timeout: float
) -> dict[str, Any]:
    latencies: list[float] = []
    passed = 0
    samples: list[dict[str, Any]] = []
    for index in range(profile.warmup + profile.iterations):
        started = time.perf_counter()
        status, body = _request(
            base_url, scenario, scenario.payload_factory(profile), timeout
        )
        elapsed_ms = (time.perf_counter() - started) * 1000
        if index < profile.warmup:
            continue
        latencies.append(elapsed_ms)
        passed += int(scenario.verifier(status, body))
        if len(samples) < 3:
            samples.append(
                {
                    "status_code": status,
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
        "iterations": profile.iterations,
        "warmup": profile.warmup,
        "pass_rate": round(passed / profile.iterations, 4),
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


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Measure a live Neurosonic backend via HTTP."
    )
    parser.add_argument(
        "--base-url", required=True, help="Running backend URL, e.g. http://127.0.0.1:8000"
    )
    parser.add_argument("--profile", choices=sorted(PROFILES), default="quick")
    parser.add_argument("--iterations", type=int)
    parser.add_argument("--warmup", type=int)
    parser.add_argument("--long-prompt-size", type=int)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--output", help="JSON result path; default is under logs/benchmarks.")
    parser.add_argument("--pretty", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    selected = PROFILES[args.profile]
    profile = TuningProfile(
        selected.name,
        args.iterations if args.iterations is not None else selected.iterations,
        args.warmup if args.warmup is not None else selected.warmup,
        args.long_prompt_size
        if args.long_prompt_size is not None
        else selected.long_prompt_size,
    )
    if (
        profile.iterations <= 0
        or profile.warmup < 0
        or profile.long_prompt_size < 16
        or args.timeout <= 0
    ):
        raise ValueError(
            "iterations > 0, warmup >= 0, long-prompt-size >= 16 dhe timeout > 0 kërkohen"
        )
    created_at = time.time()
    results = [
        _run_scenario(args.base_url, item, profile, args.timeout)
        for item in _scenarios()
    ]
    report = {
        "benchmark": "neurosonic-live-http-benchmark",
        "created_at": created_at,
        "base_url": args.base_url,
        "profile": asdict(profile),
        "totals": {
            "scenario_count": len(results),
            "overall_pass_rate": round(
                statistics.mean(item["pass_rate"] for item in results), 4
            ),
        },
        "results": results,
    }
    output_path = Path(args.output) if args.output else Path(
        "logs/benchmarks/live-benchmark-" + time.strftime("%Y%m%d-%H%M%S") + ".json"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2 if args.pretty else None) + "\n",
        encoding="utf-8",
    )
    print(f"Benchmark completed: {output_path}")
    print(
        f"Overall pass rate: {report['totals']['overall_pass_rate']:.2%} | "
        f"Scenarios: {report['totals']['scenario_count']}"
    )
    return 0 if report["totals"]["overall_pass_rate"] == 1.0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
