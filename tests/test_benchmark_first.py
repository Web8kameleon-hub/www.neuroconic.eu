from __future__ import annotations

from scripts.benchmark_first import _is_healthy


def test_health_scenario_uses_its_documented_contract() -> None:
    assert _is_healthy(200, {"status": "healthy"})
    assert not _is_healthy(200, {"success": True})
