#!/usr/bin/env python3
"""Run deterministic repository gates and optional live release checks.

The script reports the observed result of each command. It never creates tags,
pushes commits, deploys services, or treats an unavailable live backend as a
passing check.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run(name: str, command: list[str]) -> dict[str, object]:
    started = time.perf_counter()
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    return {
        "name": name,
        "command": command,
        "exit_code": result.returncode,
        "duration_ms": round((time.perf_counter() - started) * 1000, 3),
        "stdout": result.stdout[-4000:],
        "stderr": result.stderr[-4000:],
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Neurosonic release readiness gates.")
    parser.add_argument("--run-tests", action="store_true", help="Include the complete pytest suite.")
    parser.add_argument("--base-url", help="Run live trace and benchmark checks against this backend URL.")
    parser.add_argument("--benchmark-profile", choices=("quick", "standard", "stress"), default="quick")
    parser.add_argument("--output", help="Optional JSON report path.")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    checks = [
        _run("no_fake", [sys.executable, "neurosonic_no_fake_police.py", "--ci"]),
        _run("os_clx_policy", [sys.executable, "scripts/os_clx_policy_guard.py", "--strict"]),
        _run("repo_integrity", [sys.executable, "scripts/guardrails/repo_integrity_guard.py"]),
        _run("routes_history", [sys.executable, "scripts/guardrails/routes_history_guard.py"]),
        _run("compileall", [sys.executable, "-m", "compileall", "-q", "."]),
    ]
    if args.run_tests:
        checks.append(_run("pytest", [sys.executable, "-m", "pytest", "-q"]))
    else:
        checks.append(
            {
                "name": "pytest",
                "command": [],
                "exit_code": 2,
                "duration_ms": 0.0,
                "stdout": "",
                "stderr": "Missing required --run-tests release gate.",
            }
        )
    if args.base_url:
        checks.append(
            _run(
                "trace_contract",
                [
                    sys.executable,
                    "scripts/trace_uniform_check.py",
                    "--base-url",
                    args.base_url,
                ],
            )
        )
        checks.append(
            _run(
                "live_benchmark",
                [
                    sys.executable,
                    "scripts/benchmark_first.py",
                    "--base-url",
                    args.base_url,
                    "--profile",
                    args.benchmark_profile,
                ],
            )
        )
    else:
        checks.append(
            {
                "name": "live_evidence",
                "command": [],
                "exit_code": 2,
                "duration_ms": 0.0,
                "stdout": "",
                "stderr": "Missing required --base-url live release gate.",
            }
        )
    ready = all(check["exit_code"] == 0 for check in checks)
    report = {"created_at": time.time(), "ready": ready, "checks": checks}
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for check in checks:
        marker = "PASS" if check["exit_code"] == 0 else "FAIL"
        print(f"{marker} {check['name']} ({check['duration_ms']} ms)")
    print(f"RELEASE READY: {ready}")
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
