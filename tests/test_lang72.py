from __future__ import annotations

from neurosonic_lang72 import build_language_instruction, detect_language


def test_detect_language_forces_english_for_all_input() -> None:
    assert detect_language("Faleminderit shumë, si jeni sot?") == "en"
    assert detect_language("ku eshte ui per krijimin e panelit?") == "en"
    assert detect_language("Hallo, wie geht es dir heute?") == "en"
    assert detect_language("こんにちはおげんきですか") == "en"
    assert detect_language("مرحبا كيف حالك") == "en"


def test_detect_language_can_opt_out_of_english_override() -> None:
    assert detect_language("Hallo, wie geht es dir heute?", force_english=False) == "de"
    assert detect_language("Faleminderit shumë, si jeni sot?", force_english=False) == "sq"


def test_detect_language_defaults_to_english_for_short_ambiguous_text() -> None:
    assert detect_language("ok") == "en"
    assert detect_language("") == "en"


def test_build_language_instruction_requires_english_output() -> None:
    instruction = build_language_instruction("sq")
    assert "English" in instruction or "English only" in instruction
    assert "MUST" in instruction or "must" in instruction
    assert "user may write in any language" in instruction or "do not switch" in instruction.lower()


def test_build_language_instruction_can_follow_user_language_when_override_disabled() -> None:
    instruction = build_language_instruction("zz", force_english=False)
    assert "ZZ" in instruction
