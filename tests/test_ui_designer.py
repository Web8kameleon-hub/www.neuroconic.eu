from __future__ import annotations

import shutil
import subprocess

import pytest

from neurosonic_ui_designer import PersonalNodeStore, UIDesignEngine


def test_generate_schema_infers_reasoning_mode() -> None:
    engine = UIDesignEngine()
    schema = engine.generate_schema(
        prompt="Create governance and compliance dashboard",
        preferences={"title": "Gov Panel", "columns": 10},
        owner_id="user-1",
    )

    assert schema["owner_id"] == "user-1"
    assert schema["mode"] == "reasoning"
    assert schema["layout"]["columns"] == 10
    assert len(schema["widgets"]) >= 3


def test_personal_node_store_save_and_load(tmp_path) -> None:
    store = PersonalNodeStore(root_dir=str(tmp_path / "profiles"))
    schema = {"schema_version": "1.0", "widgets": [{"id": "w1", "type": "status"}]}

    saved = store.save_profile("demo_profile", schema)
    loaded = store.load_profile("demo_profile")
    listed = store.list_profiles()

    assert saved["profile_id"] == "demo_profile"
    assert loaded is not None
    assert loaded["schema"]["schema_version"] == "1.0"
    assert any(p["profile_id"] == "demo_profile" for p in listed)


def test_personal_node_store_keeps_schema_when_saving_experience_film(tmp_path) -> None:
    store = PersonalNodeStore(root_dir=str(tmp_path / "profiles"))
    schema = {"schema_version": "1.0", "widgets": [{"id": "w1", "type": "status"}]}
    store.save_profile("demo_profile", schema)

    film = {"film_version": "1.0", "profile_id": "demo_profile", "intent": "daily overview"}
    saved = store.save_experience_film("demo_profile", film)
    loaded = store.load_profile("demo_profile")

    assert saved["profile_id"] == "demo_profile"
    assert loaded["schema"]["schema_version"] == "1.0"
    assert loaded["experience_film"]["intent"] == "daily overview"


def test_plugin_address_auto_classification() -> None:
    engine = UIDesignEngine()

    email_plugin = engine.normalize_plugin("owner@example.com")
    web_plugin = engine.normalize_plugin("https://example.com/api")
    app_plugin = engine.normalize_plugin("office365://mailbox")
    local_plugin = engine.normalize_plugin("/api/internal/pulse")
    bank_plugin = engine.normalize_plugin("bank://my-bank-account")

    assert email_plugin["address_type"] == "email"
    assert web_plugin["address_type"] == "website"
    assert app_plugin["address_type"] == "app-endpoint"
    assert local_plugin["address_type"] == "internal-api"
    assert bank_plugin["address_type"] == "banking"


def test_attach_plugin_to_schema_updates_integrations() -> None:
    engine = UIDesignEngine()
    schema = engine.generate_schema(prompt="Build a creator panel")
    plugin = engine.normalize_plugin(
        address="https://plugins.neurosonic.eu/office",
        name="Office Connector",
        connector_scope="iot",
        metadata={"transport": "tide", "llm": "llama-local"},
    )

    updated = engine.attach_plugin_to_schema(schema, plugin)
    plugins = updated["integrations"]["plugins"]

    assert len(plugins) == 1
    assert plugins[0]["name"] == "Office Connector"
    assert plugins[0]["connector_scope"] == "iot"
    assert plugins[0]["service_role"] == "api-support-only"
    assert updated["dna_contract"]["immutable"] is True


def test_export_profile_to_git_requires_valid_repo(tmp_path) -> None:
    store = PersonalNodeStore(root_dir=str(tmp_path / "profiles"))
    store.save_profile("demo", {"schema_version": "1.0", "widgets": []})

    with pytest.raises(ValueError):
        store.export_profile_to_git(
            profile_id="demo",
            repository_path=str(tmp_path / "not_a_repo"),
        )


def test_export_profile_to_git_stages_file(tmp_path) -> None:
    if shutil.which("git") is None:
        pytest.skip("git executable not available")

    store = PersonalNodeStore(root_dir=str(tmp_path / "profiles"))
    store.save_profile("demo", {"schema_version": "1.0", "widgets": [{"id": "w1"}]})

    repo_path = tmp_path / "repo"
    repo_path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init"], cwd=str(repo_path), check=True, capture_output=True)

    result = store.export_profile_to_git(
        profile_id="demo",
        repository_path=str(repo_path),
        relative_output_path="exports/demo.json",
        commit=False,
    )

    exported_file = repo_path / "exports" / "demo.json"
    assert exported_file.exists()
    assert result["commit_created"] is False
    assert result["relative_path"] == "exports/demo.json"

    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=str(repo_path),
        check=True,
        capture_output=True,
        text=True,
    )
    assert "exports/demo.json" in status.stdout


def test_export_profile_to_git_rejects_parent_traversal(tmp_path) -> None:
    if shutil.which("git") is None:
        pytest.skip("git executable not available")

    store = PersonalNodeStore(root_dir=str(tmp_path / "profiles"))
    store.save_profile("demo", {"schema_version": "1.0", "widgets": []})

    repo_path = tmp_path / "repo"
    repo_path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init"], cwd=str(repo_path), check=True, capture_output=True)

    with pytest.raises(ValueError, match="escapes repository root"):
        store.export_profile_to_git(
            profile_id="demo",
            repository_path=str(repo_path),
            relative_output_path="../escape.json",
            commit=False,
        )


def test_export_profile_to_git_rejects_git_dir_targets(tmp_path) -> None:
    if shutil.which("git") is None:
        pytest.skip("git executable not available")

    store = PersonalNodeStore(root_dir=str(tmp_path / "profiles"))
    store.save_profile("demo", {"schema_version": "1.0", "widgets": []})

    repo_path = tmp_path / "repo"
    repo_path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init"], cwd=str(repo_path), check=True, capture_output=True)

    with pytest.raises(ValueError, match=r"inside \.git"):
        store.export_profile_to_git(
            profile_id="demo",
            repository_path=str(repo_path),
            relative_output_path=".git/config",
            commit=False,
        )
