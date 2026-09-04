from __future__ import annotations

from fastapi.testclient import TestClient

import backend.main as backend_main
from neurosonic_llm_bridge import LLMResult


REAL_GARBLED_REPLY = (
    "Hey! Per te mparshem per fitim, mesimaje per te jashter ne ketill per te "
    "fiton me me shkoder. Per te mparshem per fitim, mesimaje per te fiton me "
    "me shkoder. Per te arritur ne fitim te pare, mesimaje per te perdoresh "
    "konslerues te plote."
)

COHERENT_SHORT_REPLY = "Here is your weather and to-do list panel!"

COHERENT_LONG_REPLY = (
    "I created a panel with the weather widget at the top, a to-do list in "
    "the middle, and an activity tracker at the bottom. You can customize the "
    "colors and layout of the panel anytime you want, and I can also add more "
    "widgets if you tell me what you would like to see next."
)


def test_is_reply_noisy_flags_real_garbled_output() -> None:
    assert backend_main._is_reply_noisy(REAL_GARBLED_REPLY) is True


def test_is_reply_noisy_allows_coherent_short_reply() -> None:
    assert backend_main._is_reply_noisy(COHERENT_SHORT_REPLY) is False


def test_is_reply_noisy_allows_coherent_long_reply() -> None:
    assert backend_main._is_reply_noisy(COHERENT_LONG_REPLY) is False


def test_is_reply_noisy_ignores_very_short_text() -> None:
    # Below min_words threshold: not enough signal to judge, so never flagged.
    assert backend_main._is_reply_noisy("ok thanks") is False


def test_sanitize_chat_reply_keeps_short_text_unchanged() -> None:
    text = "Here is your panel!"
    assert backend_main._sanitize_chat_reply(text) == text


def test_sanitize_chat_reply_truncates_long_text() -> None:
    long_text = "word " * 300
    result = backend_main._sanitize_chat_reply(long_text)
    assert len(result) <= backend_main._UI_CHAT_MAX_REPLY_CHARS + 1
    assert result.endswith("…")


def _make_llm_result(text: str) -> LLMResult:
    return LLMResult(text=text, provider="ollama", model="deepseek-r1:7b", elapsed_ms=5.0, tokens=10)


def test_ui_chat_retries_once_on_noisy_reply_and_recovers(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(
        backend_main,
        "personal_node_store",
        backend_main.PersonalNodeStore(root_dir=str(tmp_path / "profiles")),
    )

    responses = [
        f'{{"reply": "{REAL_GARBLED_REPLY}", "title": "Panel", "widgets": []}}',
        '{"reply": "Here is your panel!", "title": "Panel", "widgets": []}',
    ]
    call_count = {"n": 0}

    def fake_generate(prompt, system=None):
        result = _make_llm_result(responses[call_count["n"]])
        call_count["n"] += 1
        return result

    monkeypatch.setattr(backend_main.llm_bridge, "generate", fake_generate)

    client = TestClient(backend_main.app)
    resp = client.post("/api/ui/chat", json={"message": "build me a panel", "profile_id": "test_retry"})

    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["reply"] == "Here is your panel!"
    assert call_count["n"] == 2


def test_ui_chat_falls_back_to_generic_reply_when_still_noisy_after_retry(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(
        backend_main,
        "personal_node_store",
        backend_main.PersonalNodeStore(root_dir=str(tmp_path / "profiles")),
    )

    def fake_generate(prompt, system=None):
        return _make_llm_result(f'{{"reply": "{REAL_GARBLED_REPLY}", "title": "Panel", "widgets": []}}')

    monkeypatch.setattr(backend_main.llm_bridge, "generate", fake_generate)

    client = TestClient(backend_main.app)
    resp = client.post("/api/ui/chat", json={"message": "build me a panel", "profile_id": "test_still_noisy"})

    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    # Never show the garbled text to the user, even though generation "succeeded".
    assert REAL_GARBLED_REPLY not in body["reply"]
    assert "trouble phrasing" in body["reply"]
