from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_module():
    path = Path("scripts/assessment_scorecard.py")
    spec = importlib.util.spec_from_file_location("assessment_scorecard", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Failed to load assessment_scorecard module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_no_go_when_hard_gate_fails() -> None:
    module = _load_module()
    payload = {
        "meta": {"project": "Neurosonic"},
        "hard_gates": {
            "security_independent_audit_passed": False,
            "gdpr_dpa_in_place": True,
            "production_release_reproducible": True,
            "critical_incident_response_tested": True,
        },
        "categories": {
            "security": {"weight": 30, "items": {"a": 5, "b": 5}},
            "privacy_sovereignty": {"weight": 20, "items": {"a": 5}},
            "reasoning_quality": {"weight": 20, "items": {"a": 5}},
            "operations_reliability": {"weight": 20, "items": {"a": 5}},
            "documentation_community": {"weight": 10, "items": {"a": 5}},
        },
    }

    report = module.evaluate(payload)

    assert report["total_score"] == 100.0
    assert report["decision"] == "No-Go"
    assert "security_independent_audit_passed" in report["failed_hard_gates"]


def test_go_when_score_high_and_gates_pass() -> None:
    module = _load_module()
    payload = {
        "meta": {"project": "Neurosonic"},
        "hard_gates": {
            "security_independent_audit_passed": True,
            "gdpr_dpa_in_place": True,
            "production_release_reproducible": True,
            "critical_incident_response_tested": True,
        },
        "categories": {
            "security": {"weight": 30, "items": {"a": 4, "b": 5}},
            "privacy_sovereignty": {"weight": 20, "items": {"a": 4}},
            "reasoning_quality": {"weight": 20, "items": {"a": 4}},
            "operations_reliability": {"weight": 20, "items": {"a": 4}},
            "documentation_community": {"weight": 10, "items": {"a": 4}},
        },
    }

    report = module.evaluate(payload)

    assert report["total_score"] >= 80
    assert report["decision"] == "Go"
