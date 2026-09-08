from __future__ import annotations

from pathlib import Path

import pytest

from neurosonic_clisonix_bridge import ClisonixAuthBillingBridge


def test_bridge_status_reports_not_configured() -> None:
    status = ClisonixAuthBillingBridge(base_url="").status()

    assert status["configured"] is False
    assert status["available"] is False
    assert "not configured" in status["reason"]


def test_bridge_rejects_insecure_cloud_endpoint_by_default() -> None:
    with pytest.raises(ValueError, match="must use HTTPS"):
        ClisonixAuthBillingBridge(base_url="http://clisonix.com")


def test_backend_runtime_exposes_cloud_bridge_status() -> None:
    source = Path("backend/main.py").read_text(encoding="utf-8")

    assert '"cloud": cloud_bridge.status()' in source
    assert '@app.get("/api/cloud/bridge")' in source
