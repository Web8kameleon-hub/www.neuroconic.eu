#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

REQUIRED_TOP_LEVEL = ["trace", "verification"]
REQUIRED_TRACE_FIELDS = ["trace_id", "input_hash", "output_hash", "pipeline"]
REQUIRED_VERIFICATION = ["reasoning_validated"]
REQUIRED_STEP_FIELDS = ["component", "status", "duration_ms", "input_hash", "output_hash"]


def main() -> int:
    import backend.main as backend_main
    from neurosonic_lightning_bridge import LightningResult, ProcessingEngine

    def _stub(
        data: str,
        engine: ProcessingEngine = ProcessingEngine.HYBRID,
        ai_enhance: bool = True,
    ) -> LightningResult:
        payload = {
            "provider": "trace-check",
            "model": "trace-check-model",
            "generated_tokens": max(16, len(data) // 4),
            "answer": "trace contract check",
            "ai_enhance": ai_enhance,
        }
        return LightningResult(
            id="trace-check",
            status="completed",
            data=payload,
            hash="tracecheckhash",
            timestamp=0.0,
            source=engine.value,
            confidence=0.95,
            error=None,
        )

    original_process = backend_main.bridge.process
    backend_main.bridge.process = _stub

    try:
        client = TestClient(backend_main.app)
        response = client.post(
            "/api/shell/think",
            json={"prompt": "Validate trace contract integrity", "task_type": "reasoning"},
        )
    finally:
        backend_main.bridge.process = original_process

    if response.status_code != 200:
        print(f"FAIL: status code {response.status_code}")
        return 1

    payload = response.json()
    failures: list[str] = []

    for field in REQUIRED_TOP_LEVEL:
        if field not in payload:
            failures.append(f"missing top-level field: {field}")

    verification = payload.get("verification", {})
    if not isinstance(verification, dict):
        failures.append("verification is not an object")
    else:
        for field in REQUIRED_VERIFICATION:
            if field not in verification:
                failures.append(f"missing verification field: {field}")

    trace = payload.get("trace", {})
    if not isinstance(trace, dict):
        failures.append("trace is not an object")
    else:
        for field in REQUIRED_TRACE_FIELDS:
            if field not in trace:
                failures.append(f"missing trace field: {field}")

        steps = trace.get("pipeline", [])
        if not isinstance(steps, list) or not steps:
            failures.append("trace.pipeline missing or empty")
        else:
            for field in REQUIRED_STEP_FIELDS:
                if field not in steps[0]:
                    failures.append(f"missing step field: {field}")

    report = {
        "status": "pass" if not failures else "fail",
        "failures": failures,
        "trace_id": trace.get("trace_id") if isinstance(trace, dict) else None,
    }

    report_path = Path("docs/production/evidence/trace_uniform_check_latest.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    if failures:
        print("FAIL: trace uniform contract check failed")
        for item in failures:
            print(f" - {item}")
        return 1

    print(f"PASS: trace uniform contract check ({report_path})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
