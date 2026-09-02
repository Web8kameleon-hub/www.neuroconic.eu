# Changelog

All notable changes to this project are documented in this file.

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
