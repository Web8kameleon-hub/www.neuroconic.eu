from __future__ import annotations

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


def test_plugin_address_auto_classification() -> None:
    engine = UIDesignEngine()

    email_plugin = engine.normalize_plugin("owner@example.com")
    web_plugin = engine.normalize_plugin("https://example.com/api")
    app_plugin = engine.normalize_plugin("office365://mailbox")
    local_plugin = engine.normalize_plugin("/api/internal/pulse")

    assert email_plugin["address_type"] == "email"
    assert web_plugin["address_type"] == "website"
    assert app_plugin["address_type"] == "app-endpoint"
    assert local_plugin["address_type"] == "internal-api"


def test_attach_plugin_to_schema_updates_integrations() -> None:
    engine = UIDesignEngine()
    schema = engine.generate_schema(prompt="Build a creator panel")
    plugin = engine.normalize_plugin(
        address="https://plugins.neurosonic.eu/office",
        name="Office Connector",
        metadata={"transport": "tide", "llm": "llama-local"},
    )

    updated = engine.attach_plugin_to_schema(schema, plugin)
    plugins = updated["integrations"]["plugins"]

    assert len(plugins) == 1
    assert plugins[0]["name"] == "Office Connector"
    assert updated["dna_contract"]["immutable"] is True
