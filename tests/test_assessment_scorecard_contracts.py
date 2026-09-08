from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def _load_module():
    path = Path("scripts/assessment_scorecard.py")
    spec = importlib.util.spec_from_file_location("assessment_scorecard", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Failed to load assessment_scorecard module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("value", [0, 1, 2.5, 5])
def test_validate_score_accepts_range(value: float) -> None:
    module = _load_module()
    assert module._validate_score(value, "field") == float(value)


@pytest.mark.parametrize("value", [-0.1, 5.1, "abc", None])
def test_validate_score_rejects_invalid_values(value: object) -> None:
    module = _load_module()
    with pytest.raises(ValueError):
        module._validate_score(value, "field")


def test_compute_category_score_calculates_weighted_score() -> None:
    module = _load_module()
    result = module._compute_category_score(
        "security",
        {"weight": 30, "items": {"a": 5, "b": 3, "c": 4}},
    )

    assert result["average"] == 4.0
    assert result["weighted_score"] == 24.0


def test_compute_category_score_requires_non_empty_items() -> None:
    module = _load_module()
    with pytest.raises(ValueError, match="must be a non-empty object"):
        module._compute_category_score("security", {"weight": 30, "items": {}})


@pytest.mark.parametrize(
    "total_score,expected",
    [
        (80.0, "Go"),
        (79.99, "Conditional"),
        (65.0, "Conditional"),
        (64.99, "No-Go"),
    ],
)
def test_decision_thresholds_without_failed_gates(
    total_score: float,
    expected: str,
) -> None:
    module = _load_module()
    decision, failed = module._decision(
        total_score,
        {
            "security_independent_audit_passed": True,
            "gdpr_dpa_in_place": True,
        },
    )

    assert decision == expected
    assert failed == []


def test_decision_fails_when_any_hard_gate_is_false() -> None:
    module = _load_module()
    decision, failed = module._decision(
        99.0,
        {
            "security_independent_audit_passed": True,
            "gdpr_dpa_in_place": False,
        },
    )

    assert decision == "No-Go"
    assert failed == ["gdpr_dpa_in_place"]


def test_to_markdown_includes_failed_gate_line() -> None:
    module = _load_module()
    markdown = module._to_markdown(
        {
            "meta": {
                "project": "Neurosonic",
                "assessor": "team",
                "date_utc": "2026-09-08T00:00:00Z",
            },
            "total_score": 50.7,
            "decision": "No-Go",
            "failed_hard_gates": ["gdpr_dpa_in_place"],
            "categories": {
                "security": {
                    "weight": 30,
                    "average": 2.0,
                    "weighted_score": 12.0,
                }
            },
        }
    )

    assert "Failed hard gates" in markdown
    assert "gdpr_dpa_in_place" in markdown


def test_evaluate_requires_non_empty_categories() -> None:
    module = _load_module()
    payload = {
        "hard_gates": {"security_independent_audit_passed": True},
        "categories": {},
    }

    with pytest.raises(ValueError, match="categories must be a non-empty object"):
        module.evaluate(payload)


def test_evaluate_requires_non_empty_hard_gates() -> None:
    module = _load_module()
    payload = {
        "hard_gates": {},
        "categories": {
            "security": {"weight": 30, "items": {"a": 4}},
        },
    }

    with pytest.raises(ValueError, match="hard_gates must be a non-empty object"):
        module.evaluate(payload)


def test_evaluate_rejects_non_object_category_payload() -> None:
    module = _load_module()
    payload = {
        "hard_gates": {"security_independent_audit_passed": True},
        "categories": {
            "security": 123,
        },
    }

    with pytest.raises(ValueError, match="categories.security must be an object"):
        module.evaluate(payload)
