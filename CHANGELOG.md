# Changelog

All notable changes to this project are documented in this file.

## v1.0.3 - 2026-09-02

Feature release focused on user-owned Git export flow for Personal Node profiles with explicit third-party liability boundaries.

### Added (v1.0.3)

- Add profile export to user-owned Git repositories with optional commit flow (`/api/ui/panels/{profile_id}/git-save`).
- Add secure repository/path validation to prevent writing outside repository root.
- Add UI controls in `personal_node/ui_composer_dynamic.html` for repository path, relative output path, commit toggle, and commit message.

### Changed (v1.0.3)

- Strengthen non-liability messaging: Neurosonic remains `api-support-only`; third-party subscriptions, billing, contracts, and credentials are user responsibility.
- Extend focused tests for Git export behavior in `tests/test_ui_designer.py`.

### Release Sync (v1.0.3)

- Git tag: `v1.0.3`
- Commit: `71be6fd`
- Release URL: <https://github.com/Web8kameleon-hub/www.neuroconic.eu/releases/tag/v1.0.3>

## v1.0.2 - 2026-09-02

Patch release focused on startup stability and popup orchestration hardening.

### Changed (v1.0.2)

- Add automatic pre-start cleanup in `start_neurosonic.ps1` for service ports `8080`, `8000`, and `5500`.
- Add `8080` preflight check in `scripts/popup_lightning.ps1` with clear PID/process diagnostics when port is occupied.
- Enable `PYTHONUTF8=1` in Lightning popup startup to avoid Windows code-page output crashes.

### Release Sync (v1.0.2)

- Git tag: `v1.0.2`
- Commit: `926c76b`
- Release URL: <https://github.com/Web8kameleon-hub/www.neuroconic.eu/releases/tag/v1.0.2>

## v1.0.1 - 2026-09-02

Patch release focused on UI selector cleanup and routing consistency.

### Changed

- Align `index.html` document language to Albanian (`lang="sq"`).
- Switch UI selector backend links to backend-relative routes (`/dashboard`, `/dna-ui`).
- Clean local editor-only noise before tagging for reproducible release state.

### Release Sync

- Git tag: `v1.0.1`
- Commit: `95a5bd1`
- Release URL: <https://github.com/Web8kameleon-hub/www.neuroconic.eu/releases/tag/v1.0.1>

## v1.0.0 - 2026-09-02

Initial public stabilization release including:

- Real shell endpoint wiring (`/api/shell/think`) without mock fallback.
- Packaging prep for PyPI, npm, and crates.
- Governance and publishing docs (`docs/deployment/PUBLISHING.md`, NodeDB Fluid shell contract).
- Repo-linking index artifacts for Web8kameleon hub.
