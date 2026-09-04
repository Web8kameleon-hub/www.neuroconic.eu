from __future__ import annotations

from neurosonic_lang72 import build_language_instruction, detect_language


def test_detect_language_albanian_with_diacritics() -> None:
    assert detect_language("Faleminderit shumë, si jeni sot?") == "sq"


def test_detect_language_albanian_ascii_no_diacritics() -> None:
    """Most Albanian users type without ë/ç on standard keyboards."""
    assert detect_language("ku eshte ui per krijimin e panelit?") == "sq"
    assert detect_language("duhet te kemi nje chat normal") == "sq"


def test_detect_language_english() -> None:
    assert detect_language("Hello, how are you today?") == "en"


def test_detect_language_german() -> None:
    assert detect_language("Hallo, wie geht es dir heute?") == "de"


def test_detect_language_defaults_to_english_for_short_ambiguous_text() -> None:
    assert detect_language("ok") == "en"
    assert detect_language("") == "en"


def test_detect_language_non_latin_script() -> None:
    assert detect_language("こんにちはおげんきですか") == "ja"
    assert detect_language("مرحبا كيف حالك") == "ar"


def test_build_language_instruction_names_language_and_requires_reply_in_it() -> None:
    instruction = build_language_instruction("sq")
    assert "Albanian" in instruction
    assert "sq" in instruction
    assert "MUST respond entirely" in instruction


def test_build_language_instruction_falls_back_to_code_for_unknown() -> None:
    instruction = build_language_instruction("zz")
    assert "ZZ" in instruction
