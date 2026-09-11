from __future__ import annotations

import json
from pathlib import Path

import backend.main as backend_main
from neurosonic_gram_adapter import CanonicalGramAdapter


def test_runtime_registry_payload_matches_installed_packages() -> None:
    """The shell registry is derived from the installed Genome, not UI literals."""
    payload = backend_main._genome_runtime_payload()

    assert payload["total"] == len(payload["packages"])
    assert all("category" in package for package in payload["packages"])


def test_dna_shell_uses_the_unified_runtime_contract() -> None:
    """The live shell reads its status and modules from the one runtime endpoint."""
    source = Path("neurosonic_dna_ui.html").read_text(encoding="utf-8")

    assert "apiGet('/api/ui/runtime')" in source
    assert "renderRuntimeCategory" in source
    assert "Quantum Package" not in source
    assert "3,847 nodes" not in source


def test_gram_adapter_reports_missing_configuration_without_fallback() -> None:
    """GRAM stays unavailable until a canonical endpoint is explicitly configured."""
    status = CanonicalGramAdapter(base_url="").status()

    assert status["configured"] is False
    assert status["available"] is False
    assert "not configured" in status["reason"]


def test_pwa_starts_in_live_shell_without_cached_html_routes() -> None:
    """Installed PWA opens the live shell and never substitutes cached page HTML."""
    manifest = json.loads(Path("manifest.webmanifest").read_text(encoding="utf-8"))
    worker = Path("service-worker.js").read_text(encoding="utf-8")

    assert manifest["start_url"] == "/dna-ui"
    assert "event.request.mode === 'navigate'" in worker
    assert "'/ui-composer'" not in worker


def test_ui_composer_uses_live_panel_services() -> None:
    """Composer requests panels from the backend instead of constructing browser-only data."""
    source = Path("personal_node/ui_composer_dynamic.html").read_text(encoding="utf-8")

    assert 'postJson("/api/ui/chat"' in source
    assert 'postJson("/api/ui/design"' in source
    assert 'getJson("/api/ui/runtime")' in source
    assert "buildDynamicWorkspace" not in source
    assert "Mock Magic" not in source


def test_rolling_deploy_retries_the_real_think_smoke() -> None:
    """A transient proxy response must not abort a healthy rolling update."""
    source = Path("scripts/rolling_update_backends.sh").read_text(encoding="utf-8")

    assert "wait_think_smoke()" in source
    assert 'wait_think_smoke "$THINK_URL" "$HEALTH_TIMEOUT_SECONDS" "$POLL_INTERVAL_SECONDS"' in source
