from __future__ import annotations

import io
import json
from pathlib import Path
from urllib.error import HTTPError

import neurosonic_clisonix_bridge as bridge_module
from neurosonic_clisonix_bridge import ClisonixAuthBillingBridge, ClisonixBridgeError


class _FakeResponse:
    def __init__(self, payload: dict[str, object]):
        self._payload = json.dumps(payload).encode("utf-8")

    def read(self) -> bytes:
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_bridge_status_reports_not_configured() -> None:
    status = ClisonixAuthBillingBridge(base_url="").status()

    assert status["configured"] is False
    assert status["available"] is False
    assert "not configured" in status["reason"]


def test_bridge_login_posts_to_configured_service(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["method"] = request.get_method()
        captured["body"] = request.data.decode("utf-8") if request.data else ""
        captured["auth"] = request.headers.get("Authorization")
        return _FakeResponse({"token": "ok"})

    monkeypatch.setattr(bridge_module, "urlopen", fake_urlopen)

    bridge = ClisonixAuthBillingBridge(base_url="https://clisonix.com")
    result = bridge.login("user@example.com", "secret-123")

    assert result == {"token": "ok"}
    assert captured["url"] == "https://clisonix.com/api/auth/login"
    assert captured["method"] == "POST"
    assert json.loads(str(captured["body"]))["email"] == "user@example.com"


def test_bridge_http_error_detail_is_returned(monkeypatch) -> None:
    def fake_urlopen(request, timeout):
        raise HTTPError(
            url=request.full_url,
            code=401,
            msg="Unauthorized",
            hdrs=None,
            fp=io.BytesIO(b'{"detail":"Invalid upstream token"}'),
        )

    monkeypatch.setattr(bridge_module, "urlopen", fake_urlopen)

    bridge = ClisonixAuthBillingBridge(base_url="https://clisonix.com")
    try:
        bridge.billing_status("Bearer abc")
    except ClisonixBridgeError as exc:
        assert "Invalid upstream token" in str(exc)
    else:
        raise AssertionError("Expected ClisonixBridgeError")


def test_backend_runtime_exposes_cloud_bridge_status() -> None:
    source = Path("backend/main.py").read_text(encoding="utf-8")

    assert '"cloud": cloud_bridge.status()' in source
    assert '@app.get("/api/cloud/bridge")' in source
