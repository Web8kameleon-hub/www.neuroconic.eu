#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable

from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import backend.main as backend_main
from neurosonic_lightning_bridge import LightningResult, ProcessingEngine


@dataclass
class TuningProfile:
    name: str
    iterations: int
    warmup: int
    long_prompt_size: int


@dataclass
class Scenario:
    name: str
    endpoint: str
    method: str
    payload_factory: Callable[[TuningProfile], dict[str, Any]]
    expected_status: int
    verifier: Callable[[dict[str, Any]], bool]
    mode: str


PROFILES: dict[str, TuningProfile] = {
    "quick": TuningProfile(name="quick", iterations=10, warmup=2, long_prompt_size=2048),
    "standard": TuningProfile(name="standard", iterations=50, warmup=5, long_prompt_size=8192),
    "stress": TuningProfile(name="stress", iterations=200, warmup=15, long_prompt_size=32768),
}


def _percentile(sorted_values: list[float], q: float) -> float:
    if not sorted_values:
        return 0.0
    if len(sorted_values) == 1:
        return sorted_values[0]
    index = (len(sorted_values) - 1) * q
    low = int(index)
    high = min(low + 1, len(sorted_values) - 1)
    weight = index - low
    return sorted_values[low] * (1.0 - weight) + sorted_values[high] * weight


def _build_stub(mode: str) -> Callable[..., LightningResult]:
    def _process(data: str, engine=ProcessingEngine.HYBRID, ai_enhance: bool = True) -> LightningResult:
        if mode == "echo":
            payload: Any = data
        elif mode == "error":
            payload = None
        else:
            payload = {
                "provider": "benchmark-runtime",
                "model": "benchmark-model-v1",
                "generated_tokens": max(16, min(256, len(data) // 4)),
                "answer": f"Processed {len(data)} chars safely",
            }

        status = "error" if mode == "error" else "completed"
        error = "simulated_runtime_error" if mode == "error" else None
        return LightningResult(
            id="bench",
            status=status,
            data=payload,
            hash="benchhash123",
            timestamp=time.time(),
            source=(engine.value if isinstance(engine, ProcessingEngine) else str(engine)),
            confidence=0.95,
            error=error,
        )

    return _process


def _verify_shell_success(payload: dict[str, Any]) -> bool:
    return (
        payload.get("success") is True
        and payload.get("status") == "completed"
        and payload.get("verification", {}).get("reasoning_validated") is True
    )


def _verify_shell_empty(payload: dict[str, Any]) -> bool:
    return payload.get("success") is False and payload.get("error") == "Prompt is empty"


def _verify_shell_degraded(payload: dict[str, Any]) -> bool:
    return (
        payload.get("success") is False
        and payload.get("status") == "degraded"
        and payload.get("trace", {}).get("echo_detected") is True
    )


def _verify_plugin_private(payload: dict[str, Any]) -> bool:
    return payload.get("success") is False and "private or local network" in str(payload.get("error", ""))


def _verify_plugin_sensitive(payload: dict[str, Any]) -> bool:
    return payload.get("success") is False and "sensitive key" in str(payload.get("error", ""))


def _verify_plugin_success(payload: dict[str, Any]) -> bool:
    return payload.get("success") is True and payload.get("dna_immutable") is True


def _build_scenarios() -> list[Scenario]:
    return [
        Scenario(
            name="shell_think_reasoning_success",
            endpoint="/api/shell/think",
            method="POST",
            payload_factory=lambda _: {
                "prompt": "Analyze policy conflicts and propose safe resolution.",
                "task_type": "reasoning",
            },
            expected_status=200,
            verifier=_verify_shell_success,
            mode="success",
        ),
        Scenario(
            name="shell_think_empty_prompt_edge",
            endpoint="/api/shell/think",
            method="POST",
            payload_factory=lambda _: {
                "prompt": "   ",
                "task_type": "reasoning",
            },
            expected_status=200,
            verifier=_verify_shell_empty,
            mode="success",
        ),
        Scenario(
            name="shell_think_echo_edge",
            endpoint="/api/shell/think",
            method="POST",
            payload_factory=lambda _: {
                "prompt": "go or no go",
                "task_type": "reasoning",
            },
            expected_status=200,
            verifier=_verify_shell_degraded,
            mode="echo",
        ),
        Scenario(
            name="shell_think_long_prompt_tuning",
            endpoint="/api/shell/think",
            method="POST",
            payload_factory=lambda profile: {
                "prompt": "A" * profile.long_prompt_size,
                "task_type": "reasoning",
            },
            expected_status=200,
            verifier=_verify_shell_success,
            mode="success",
        ),
        Scenario(
            name="plugin_attach_private_network_edge",
            endpoint="/api/ui/plugins/bench-profile",
            method="POST",
            payload_factory=lambda _: {
                "address": "http://127.0.0.1:8080",
                "liability_ack": True,
            },
            expected_status=200,
            verifier=_verify_plugin_private,
            mode="success",
        ),
        Scenario(
            name="plugin_attach_sensitive_metadata_edge",
            endpoint="/api/ui/plugins/bench-profile",
            method="POST",
            payload_factory=lambda _: {
                "address": "https://plugins.example.com/secure",
                "liability_ack": True,
                "metadata": {"api_key": "x"},
            },
            expected_status=200,
            verifier=_verify_plugin_sensitive,
            mode="success",
        ),
        Scenario(
            name="plugin_attach_success_baseline",
            endpoint="/api/ui/plugins/bench-profile",
            method="POST",
            payload_factory=lambda _: {
                "address": "https://plugins.example.com/connector",
                "liability_ack": True,
                "metadata": {"region": "eu-west"},
            },
            expected_status=200,
            verifier=_verify_plugin_success,
            mode="success",
        ),
    ]


def _run_scenario(client: TestClient, scenario: Scenario, profile: TuningProfile) -> dict[str, Any]:
    latencies_ms: list[float] = []
    pass_count = 0
    samples: list[dict[str, Any]] = []
    total_calls = profile.iterations + profile.warmup

    original_process = backend_main.bridge.process
    backend_main.bridge.process = _build_stub(scenario.mode)
    try:
        for call_index in range(total_calls):
            payload = scenario.payload_factory(profile)
            started = time.perf_counter()
            response = client.request(scenario.method, scenario.endpoint, json=payload)
            elapsed_ms = (time.perf_counter() - started) * 1000

            if call_index >= profile.warmup:
                latencies_ms.append(elapsed_ms)
                body = response.json()
                ok = response.status_code == scenario.expected_status and scenario.verifier(body)
                pass_count += int(ok)
                if len(samples) < 3:
                    samples.append(
                        {
                            "status_code": response.status_code,
                            "success": body.get("success"),
                            "status": body.get("status"),
                            "error": body.get("error"),
                        }
                    )
    finally:
        backend_main.bridge.process = original_process

    sorted_latencies = sorted(latencies_ms)
    total_duration_s = sum(latencies_ms) / 1000 if latencies_ms else 0.0
    throughput_rps = (len(latencies_ms) / total_duration_s) if total_duration_s > 0 else 0.0
    mean_ms = statistics.mean(latencies_ms) if latencies_ms else 0.0
    stdev_ms = statistics.pstdev(latencies_ms) if len(latencies_ms) > 1 else 0.0

    return {
        "name": scenario.name,
        "endpoint": scenario.endpoint,
        "iterations": profile.iterations,
        "warmup": profile.warmup,
        "pass_rate": (pass_count / profile.iterations) if profile.iterations else 0.0,
        "throughput_rps": round(throughput_rps, 3),
        "latency_ms": {
            "min": round(sorted_latencies[0], 3) if sorted_latencies else 0.0,
            "p50": round(_percentile(sorted_latencies, 0.50), 3),
            "p95": round(_percentile(sorted_latencies, 0.95), 3),
            "max": round(sorted_latencies[-1], 3) if sorted_latencies else 0.0,
            "mean": round(mean_ms, 3),
            "stdev": round(stdev_ms, 3),
        },
        "samples": samples,
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Neurosonic first benchmark: baseline, tuning and edge-case scenarios."
    )
    parser.add_argument(
        "--profile",
        choices=sorted(PROFILES.keys()),
        default="quick",
        help="Tuning profile to run.",
    )
    parser.add_argument("--iterations", type=int, default=None, help="Override profile iterations.")
    parser.add_argument("--warmup", type=int, default=None, help="Override warmup iterations.")
    parser.add_argument(
        "--long-prompt-size",
        type=int,
        default=None,
        help="Override long prompt size used in edge scenario.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output JSON file path. Default: logs/benchmarks/first-benchmark-<ts>.json",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    selected = PROFILES[args.profile]
    profile = TuningProfile(
        name=selected.name,
        iterations=args.iterations if args.iterations is not None else selected.iterations,
        warmup=args.warmup if args.warmup is not None else selected.warmup,
        long_prompt_size=(
            args.long_prompt_size
            if args.long_prompt_size is not None
            else selected.long_prompt_size
        ),
    )

    if profile.iterations <= 0:
        raise ValueError("iterations must be > 0")
    if profile.warmup < 0:
        raise ValueError("warmup must be >= 0")
    if profile.long_prompt_size < 16:
        raise ValueError("long_prompt_size must be >= 16")

    started = time.time()
    client = TestClient(backend_main.app)
    scenarios = _build_scenarios()
    results = [_run_scenario(client, scenario, profile) for scenario in scenarios]

    overall_pass_rate = statistics.mean([entry["pass_rate"] for entry in results]) if results else 0.0
    output = {
        "benchmark": "neurosonic-first-benchmark",
        "created_at": started,
        "profile": asdict(profile),
        "totals": {
            "scenario_count": len(results),
            "overall_pass_rate": round(overall_pass_rate, 4),
        },
        "results": results,
    }

    output_path = Path(args.output) if args.output else Path(
        "logs/benchmarks/first-benchmark-" + time.strftime("%Y%m%d-%H%M%S") + ".json"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2 if args.pretty else None, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Benchmark completed: {output_path}")
    print(
        "Overall pass rate: "
        f"{output['totals']['overall_pass_rate']:.2%} | "
        f"Scenarios: {output['totals']['scenario_count']} | "
        f"Profile: {profile.name}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())