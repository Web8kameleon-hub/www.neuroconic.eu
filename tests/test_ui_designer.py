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
