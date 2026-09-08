from __future__ import annotations

import backend.main as backend_main
from neurosonic_lightning_bridge import ProcessingEngine


def test_echo_normalization_detects_equivalent_text() -> None:
    prompt = "Go   or\nno go"
    response = "  go or no GO  "

    assert backend_main._normalize_for_echo(prompt) == backend_main._normalize_for_echo(response)


def test_runtime_metadata_extracts_real_bridge_fields() -> None:
    provider, model, generated_tokens = backend_main._extract_runtime_metadata(
        {
            "provider": "ollama",
            "model_name": "llama3.1:8b",
            "eval_count": "84",
        }
    )

    assert provider == "ollama"
    assert model == "llama3.1:8b"
    assert generated_tokens == 84


def test_runtime_metadata_rejects_non_numeric_token_values() -> None:
    provider, model, generated_tokens = backend_main._extract_runtime_metadata(
        {"source": "bridge", "model": "local", "tokens": "unknown"}
    )

    assert provider == "bridge"
    assert model == "local"
    assert generated_tokens is None


def test_trace_step_has_required_contract_fields() -> None:
    trace = backend_main._trace_step(
        step="validator",
        component="pipeline.validator",
        entered=True,
        status="ok",
        duration_ms=12.34567,
        input_hash_value="input",
        output_hash_value="output",
        details={"reasoning_validated": True},
    )

    assert trace == {
        "step": "validator",
        "component": "pipeline.validator",
        "entered": True,
        "status": "ok",
        "duration_ms": 12.346,
        "input_hash": "input",
        "output_hash": "output",
        "details": {"reasoning_validated": True},
    }


def test_xcl_engine_generation_params_are_fully_deterministic() -> None:
    params = backend_main._generation_params_for_engine(ProcessingEngine.XCL)

    assert params == {"temperature": 0.0, "top_p": 1.0}
