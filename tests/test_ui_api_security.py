from __future__ import annotations

from fastapi.testclient import TestClient

import backend.main as backend_main
from neurosonic_ui_designer import PersonalNodeStore


def test_ui_design_ignores_body_owner_id_and_uses_trusted_header(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(
        backend_main,
        "personal_node_store",
        PersonalNodeStore(root_dir=str(tmp_path / "profiles")),
    )
    client = TestClient(backend_main.app)

    response = client.post(
        "/api/ui/design",
        json={
            "prompt": "build panel",
            "profile_id": "sec-owner",
            "owner_id": "untrusted-body-owner",
            "save": False,
        },
        headers={"x-neurosonic-owner-id": "trusted-owner-1"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["schema"]["owner_id"] == "trusted-owner-1"


def test_ui_plugin_attach_rejects_private_network_address(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(
        backend_main,
        "personal_node_store",
        PersonalNodeStore(root_dir=str(tmp_path / "profiles")),
    )
    client = TestClient(backend_main.app)

    response = client.post(
        "/api/ui/plugins/sec-profile",
        json={
            "address": "http://127.0.0.1:8080",
            "liability_ack": True,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is False
    assert "private or local network" in payload["error"]


def test_ui_plugin_attach_rejects_internal_path_address(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(
        backend_main,
        "personal_node_store",
        PersonalNodeStore(root_dir=str(tmp_path / "profiles")),
    )
    client = TestClient(backend_main.app)

    response = client.post(
        "/api/ui/plugins/sec-profile",
        json={
            "address": "/api/internal/admin",
            "liability_ack": True,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is False
    assert "internal paths" in payload["error"]


def test_ui_plugin_attach_rejects_sensitive_metadata_keys(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(
        backend_main,
        "personal_node_store",
        PersonalNodeStore(root_dir=str(tmp_path / "profiles")),
    )
    client = TestClient(backend_main.app)

    response = client.post(
        "/api/ui/plugins/sec-profile",
        json={
            "address": "https://plugins.example.com/connector",
            "liability_ack": True,
            "metadata": {"api_key": "secret-value"},
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is False
    assert "sensitive key" in payload["error"]
