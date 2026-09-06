from fastapi.testclient import TestClient

import backend.main as backend_main
from neurosonic_lightning_bridge import LightningResult, ProcessingEngine
from neurosonic_llm_bridge import LLMResult


def _make_result(data, status: str = "completed", error: str | None = None) -> LightningResult:
    return LightningResult(
        id="proc_test",
        status=status,
        data=data,
        hash="abc123hash",
        timestamp=0.0,
        source=ProcessingEngine.CLX.value,
        confidence=0.9,
        error=error,
    )


def _make_llm_result(text: str, provider: str = "ollama", model: str = "qwen2.5:7b", tokens: int | None = None) -> LLMResult:
    return LLMResult(text=text, provider=provider, model=model, elapsed_ms=5.0, tokens=tokens)


def test_shell_think_flags_echo_as_degraded(monkeypatch) -> None:
    prompt = "go or no go"

    def stub_process(data, engine=ProcessingEngine.HYBRID, ai_enhance=True):
        return _make_result("bridge-ok")

    def stub_generate(text, system=None, temperature=None, top_p=None):
        return _make_llm_result(prompt)

    monkeypatch.setattr(backend_main.bridge, "process", stub_process)
    monkeypatch.setattr(backend_main.llm_bridge, "generate", stub_generate)

    client = TestClient(backend_main.app)
    response = client.post(
        "/api/shell/think",
        json={"prompt": prompt, "task_type": "reasoning"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is False
    assert payload["status"] == "degraded"
    assert payload["trace"]["echo_detected"] is True
    assert payload["verification"]["reasoning_validated"] is False
    assert payload["response"] == ""
    assert payload["raw_response"].strip().lower() == prompt


def test_shell_think_returns_provider_metadata_when_reasoning_valid(monkeypatch) -> None:
    prompt = "explain governance policy conflicts"

    def stub_process(data, engine=ProcessingEngine.HYBRID, ai_enhance=True):
        return _make_result("bridge-ok")

    def stub_generate(text, system=None, temperature=None, top_p=None):
        return _make_llm_result(
            "Policy conflicts can be resolved by explicit precedence rules.",
            provider="ollama",
            model="llama3.1:8b",
            tokens=84,
        )

    monkeypatch.setattr(backend_main.bridge, "process", stub_process)
    monkeypatch.setattr(backend_main.llm_bridge, "generate", stub_generate)

    client = TestClient(backend_main.app)
    response = client.post(
        "/api/shell/think",
        json={"prompt": prompt, "task_type": "reasoning"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["execution"] == "completed"
    assert payload["provider"] == "ollama"
    assert payload["model"] == "llama3.1:8b"
    assert payload["generated_tokens"] == 84
    assert payload["trace"]["echo_detected"] is False
    assert payload["verification"]["reasoning_validated"] is True


def test_shell_think_trace_contains_required_pipeline_steps(monkeypatch) -> None:
    prompt = "Analyze governance policy conflicts"

    def stub_process(data, engine=ProcessingEngine.HYBRID, ai_enhance=True):
        return _make_result("bridge-ok")

    def stub_generate(text, system=None, temperature=None, top_p=None):
        return _make_llm_result("Structured answer that is not an echo")

    monkeypatch.setattr(backend_main.bridge, "process", stub_process)
    monkeypatch.setattr(backend_main.llm_bridge, "generate", stub_generate)

    client = TestClient(backend_main.app)
    response = client.post(
        "/api/shell/think",
        json={"prompt": prompt, "task_type": "reasoning"},
    )

    assert response.status_code == 200
    payload = response.json()
    pipeline = payload["trace"]["pipeline"]

    required_steps = [
        "scanner",
        "intent",
        "planner",
        "memory",
        "knowledge",
        "reasoning",
        "validator",
        "response",
    ]

    pipeline_by_step = {entry["step"]: entry for entry in pipeline}
    for step in required_steps:
        assert step in pipeline_by_step
        entry = pipeline_by_step[step]
        assert "component" in entry
        assert "entered" in entry
        assert "status" in entry
        assert "input_hash" in entry
        assert "output_hash" in entry
        assert "duration_ms" in entry


def test_xcl_engine_generation_params_are_fully_deterministic() -> None:
    # XCL is Neurosonic's designated code engine and must never behave like
    # a "creative" chat engine: temperature=0, top_p=1 means greedy/argmax
    # decoding (always pick the single highest-probability next token), so
    # the exact same prompt always produces the exact same output. This
    # guards against a future change accidentally reintroducing randomness
    # for code generation.
    params = backend_main._generation_params_for_engine(ProcessingEngine.XCL)
    assert params["temperature"] == 0.0
    assert params["top_p"] == 1.0


def test_shell_think_passes_deterministic_params_for_code_task(monkeypatch) -> None:
    prompt = "write a function"
    captured: dict[str, object] = {}

    def stub_process(data, engine=ProcessingEngine.HYBRID, ai_enhance=True):
        return _make_result("bridge-ok")

    def stub_generate(text, system=None, temperature=None, top_p=None):
        captured["temperature"] = temperature
        captured["top_p"] = top_p
        return _make_llm_result("def add(a, b):\n    return a + b")

    monkeypatch.setattr(backend_main.bridge, "process", stub_process)
    monkeypatch.setattr(backend_main.llm_bridge, "generate", stub_generate)

    client = TestClient(backend_main.app)
    response = client.post(
        "/api/shell/think",
        json={"prompt": prompt, "task_type": "code"},
    )

    assert response.status_code == 200
    assert response.json()["engine"] == "xcl"
    assert captured["temperature"] == 0.0
    assert captured["top_p"] == 1.0
