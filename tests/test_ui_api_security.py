from __future__ import annotations

import pytest
from starlette.requests import Request

import backend.main as backend_main


def _request_with_owner(owner_id: str) -> Request:
    return Request(
        {
            "type": "http",
            "method": "POST",
            "scheme": "https",
            "path": "/api/ui/design",
            "headers": [(b"x-neurosonic-owner-id", owner_id.encode("ascii"))],
        }
    )


def test_owner_resolution_uses_valid_request_header() -> None:
    request = _request_with_owner("trusted-owner-1")

    assert backend_main._resolve_trusted_owner_id(request) == "trusted-owner-1"


def test_plugin_address_rejects_private_network() -> None:
    with pytest.raises(ValueError, match="private or local network"):
        backend_main._validate_plugin_address("http://127.0.0.1:8080")


def test_plugin_address_rejects_internal_path() -> None:
    with pytest.raises(ValueError, match="internal paths"):
        backend_main._validate_plugin_address("/api/internal/admin")


def test_plugin_metadata_rejects_sensitive_key_names() -> None:
    with pytest.raises(ValueError, match="sensitive key"):
        backend_main._validate_plugin_metadata({"api_key": "not-accepted"})
