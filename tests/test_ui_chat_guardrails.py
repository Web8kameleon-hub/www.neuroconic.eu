from __future__ import annotations

import backend.main as backend_main


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
    long_text = "word " * (backend_main._UI_CHAT_MAX_REPLY_CHARS // 5 + 200)
    result = backend_main._sanitize_chat_reply(long_text)
    assert len(result) <= backend_main._UI_CHAT_MAX_REPLY_CHARS + 1
    assert result.endswith("…")
