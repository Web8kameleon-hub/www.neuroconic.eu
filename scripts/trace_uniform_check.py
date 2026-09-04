#!/usr/bin/env python3
"""Validate the trace contract returned by a running Neurosonic backend."""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

REQUIRED_TOP_LEVEL = ("trace", "verification")
REQUIRED_TRACE_FIELDS = ("trace_id", "input_hash", "output_hash", "pipeline")
REQUIRED_STEP_FIELDS = ("component", "status", "duration_ms", "input_hash", "output_hash")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate /api/shell/think trace fields against a live backend."
    )
    parser.add_argument(
        "--base-url", required=True, help="Running backend URL, e.g. http://127.0.0.1:8000"
    )
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument(
        "--output", default="docs/production/evidence/trace_uniform_check_latest.json"
    )
    return parser.parse_args()


def _request(base_url: str, timeout: float) -> tuple[int, dict[str, Any]]:
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/api/shell/think",
        data=json.dumps(
            {"prompt": "Validate trace contract integrity", "task_type": "reasoning"}
        ).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = response.status
            raw = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as error:
        status = error.code
        raw = error.read().decode("utf-8", errors="replace")
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError("Server returned a non-object JSON response")
    return status, payload


def main() -> int:
    args = _parse_args()
    if args.timeout <= 0:
        raise ValueError("timeout must be greater than zero")
    status, payload = _request(args.base_url, args.timeout)
    failures: list[str] = []
    if not 200 <= status < 300:
        failures.append(f"unexpected status code: {status}")
    for field in REQUIRED_TOP_LEVEL:
        if field not in payload:
            failures.append(f"missing top-level field: {field}")
    trace = payload.get("trace")
    verification = payload.get("verification")
    if not isinstance(verification, dict) or "reasoning_validated" not in verification:
        failures.append("missing verification.reasoning_validated")
    if not isinstance(trace, dict):
        failures.append("trace is not an object")
        trace = {}
    for field in REQUIRED_TRACE_FIELDS:
        if field not in trace:
            failures.append(f"missing trace field: {field}")
    steps = trace.get("pipeline")
    if not isinstance(steps, list) or not steps:
        failures.append("trace.pipeline missing or empty")
    elif not all(
        isinstance(step, dict) and all(field in step for field in REQUIRED_STEP_FIELDS)
        for step in steps
    ):
        failures.append("one or more pipeline steps miss required fields")
    report = {
        "status": "pass" if not failures else "fail",
        "base_url": args.base_url,
        "http_status": status,
        "failures": failures,
        "trace_id": trace.get("trace_id"),
    }
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if failures:
        print("FAIL: trace uniform contract check failed")
        for failure in failures:
            print(f" - {failure}")
        return 1
    print(f"PASS: trace uniform contract check ({path})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
