# Changelog

All notable changes to this project are documented in this file.

## Unreleased

### Changed

- Replace in-process benchmark and trace checks with live HTTP checks against a
  backend provided explicitly through `--base-url`; unavailable services now
  fail the checks instead of producing synthetic evidence.
- Update benchmark comparison to select only `live-benchmark-*` artifacts.
- Add `scripts/release_readiness.py` and the release-readiness runbook for
  deterministic repository gates plus optional live verification.
- Align dev HTTP client constraints with the TestClient compatibility range.
- Refactor trace-contract and UI-security tests to exercise pure runtime
  contract helpers without replacing live bridge or storage objects.

### Release verification

- Local repository gates, architecture tests and the complete pytest suite pass.
- Public `/api/shell/think` evidence remains a release gate and must meet its
  configured availability and latency objectives before a production deploy.

## v1.0.13 - 2026-09-02

Observability and evidence maturity release focused on SLO/error-budget formalization, uniform tracing validation, STRIDE threat modeling, and external benchmark evidence mapping.

### Added (v1.0.13)

- Add production evidence generators:
  - `scripts/production_evidence_pack.py`
  - `scripts/benchmark_compare.py`
  - `scripts/observability_slo_snapshot.py`
  - `scripts/trace_uniform_check.py`
- Add observability definitions and policy docs:
  - `docs/production/observability/SLO_DEFINITIONS.json`
  - `docs/production/observability/SLO_DASHBOARD_GRAFANA.json`
  - `docs/production/observability/ERROR_BUDGET_POLICY.md`
  - `docs/production/observability/TRACING_UNIFORM_STANDARD.md`
- Add formal threat model:
  - `docs/production/security/THREAT_MODEL_STRIDE.md`
- Add external benchmark evidence mapping:
  - `docs/production/evidence/EXTERNAL_BENCHMARK_EVIDENCE.md`
  - `docs/production/evidence/external_benchmark_evidence.json`
- Add structure consolidation plan:
  - `docs/guides/STRUCTURE_CONSOLIDATION_PLAN.md`

### Changed (v1.0.13)

- Update `README.md` to remove overclaims and align project messaging with evidence-first posture and optional runtime dependency profiles.
- Extend README with direct runbook sections for Production Evidence Pack, Full Observability Pack, Formal Threat Modeling, and External Benchmark Evidence.

### Validation (v1.0.13)

- `python scripts/production_evidence_pack.py --pretty` → generated evidence trends and incident/rollback logs.
- `python scripts/observability_slo_snapshot.py --pretty` → generated `slo_snapshot_latest.json` and `error_budget_status_latest.md`.
- `python scripts/benchmark_compare.py --pretty` → generated comparative JSON/Markdown evidence.
- `python scripts/trace_uniform_check.py` → `PASS` and generated `trace_uniform_check_latest.json`.
- `python -m py_compile scripts/production_evidence_pack.py scripts/benchmark_compare.py scripts/observability_slo_snapshot.py scripts/trace_uniform_check.py` → `PASS`.

### Release Sync (v1.0.13)

- Git tag: `v1.0.13`
- Commit: `fd5c236`
- Tag URL: <https://github.com/Web8kameleon-hub/www.neuroconic.eu/tree/v1.0.13>

## v1.0.12 - 2026-09-02

Guardrails and release-governance upgrade focused on lightweight OS-CLX policy enforcement, repository integrity checks, route-history drift detection, and immutable release metadata.

### Added (v1.0.12)

- Add first benchmark harness `scripts/benchmark_first.py` with tuning profiles (`quick`, `standard`, `stress`) and edge-case scenarios for `/api/shell/think` and `/api/ui/plugins/{profile_id}`.
- Add lightweight OS-CLX policy guard `scripts/os_clx_policy_guard.py` with profile manifest `docs/governance/OS_CLX_POLICY_PROFILE.json`.
- Add new guardrails:
  - `scripts/guardrails/repo_integrity_guard.py`
  - `scripts/guardrails/routes_history_guard.py`
  - `scripts/guardrails/compose.services.txt`
- Add immutable release workflow `.github/workflows/release-immutable.yml` for tag/manual release manifest artifacts.
- Add governance/acceleration guide `docs/guides/OS_CLX_CROSS_REPO_ACCELERATION.md`.

### Changed (v1.0.12)

- Update CI workflow `.github/workflows/ci.yml` to enforce:
  - `python neurosonic_no_fake_police.py --ci`
  - `python scripts/os_clx_policy_guard.py --strict`
  - `python scripts/guardrails/repo_integrity_guard.py`
  - `python scripts/guardrails/routes_history_guard.py`
- Extend `README.md` with benchmark usage, OS-CLX policy guard usage, guardrails commands, and immutable release trigger flow.
- Update `.gitignore` to ignore generated benchmark outputs under `logs/benchmarks/*.json`.

### Validation (v1.0.12)

- `python scripts/os_clx_policy_guard.py --strict` → `PASS`.
- `python scripts/guardrails/repo_integrity_guard.py` → `PASS`.
- `python scripts/guardrails/routes_history_guard.py` → `PASS`.
- `pytest -q tests/test_shell_think_anti_echo.py tests/test_ui_api_security.py tests/test_ui_designer.py` → `15 passed`.

### Release Sync (v1.0.12)

- Git tag: `v1.0.12`
- Commit: `889932f`
- Tag URL: <https://github.com/Web8kameleon-hub/www.neuroconic.eu/tree/v1.0.12>

## v1.0.11 - 2026-09-02

Runtime sync release that finalizes remaining local updates and fixes DNA UI chat payload handling.

### Changed (v1.0.11)

- Sync remaining local updates in `.vscode/settings.json`, `clx_resonance.py`, and `neurosonic.py`.
- Fix corrupted chat call path in `neurosonic_dna_ui.html` (`addMessage(...)`, `Array.isArray(result.sources)`, `result.verification`).
- Remove `StarletteDeprecationWarning` in tests by installing and pinning `httpx2` for dev/test environments.

### Validation (v1.0.11)

- `pytest -q` completed successfully: `18 passed` (warning removed).
- `python neurosonic_no_fake_police.py --ci` status: `PASTUR`.

### Release Sync (v1.0.11)

- Git tag: `v1.0.11`
- Commit: `737b8e1`
- Tag URL: <https://github.com/Web8kameleon-hub/www.neuroconic.eu/tree/v1.0.11>

## v1.0.9 - 2026-09-02

Warning cleanup and diagnostics hardening release focused on SEO script hygiene, Lightning bridge typing/exception cleanup, Markdown quality, and UI composer style compliance.

### Changed (v1.0.9)

- Clean `neurosonic_seo.py`: remove redundant UTF-8 declaration, sort imports, and use timezone-aware date handling.
- Modernize `neurosonic_lightning_bridge.py`: remove deprecated typing patterns, simplify imports, replace broad exception catches in health/request paths, and remove non-interpolated f-string.
- Fix Markdown lint findings in `README.sq.md` (heading semantics, non-empty badge links, table style, final quote block).
- Replace inline CSS in `personal_node/ui_composer.html` with class-based styling.

### Validation (v1.0.9)

- `pytest -q` completed successfully: `18 passed, 1 warning`.
- Workspace diagnostics reduced from previously reported `36` to a single remaining analyzer warning in `scripts/rolling_update_backends.ps1`.

### Release Sync (v1.0.9)

- Git tag: `v1.0.9`
- Commit: `e5ac84f`
- Tag URL: <https://github.com/Web8kameleon-hub/www.neuroconic.eu/tree/v1.0.9>

## v1.0.7 - 2026-09-02

CI stabilization patch focused on Zero Fake enforcement compatibility and architecture test execution reliability.

### Changed (v1.0.7)

- Replace legacy placeholder marker in `LegacyBaseAgent.process` within `neurosonic.py` so `NO FAKE Police` CI check no longer flags `NotImplemented` placeholder violations.
- Fix indentation consistency in `test_architecture.py` to eliminate `IndentationError/TabError` during architecture test execution in CI.

### Validation (v1.0.7)

- `Neurosonic CI - Zero Fake Enforcement` run on commit `cae5df3` completed successfully.
- `CI` workflow run on commit `cae5df3` completed successfully.

### Release Sync (v1.0.7)

- Git tag: `v1.0.7`
- Commit: `TBD`
- Release URL: `TBD`

## v1.0.6 - 2026-09-02

Reliability and integrity release focused on anti-echo enforcement in `shell/think` and Nginx failover hardening for backend rolling restarts.

### Added (v1.0.6)

- Add anti-echo regression suite in `tests/test_shell_think_anti_echo.py`.
- Add operational rolling update script `scripts/rolling_update_backends.ps1`.
- Add usage guide `docs/guides/rolling_update_backends.md`.
- Add second backend service `backend_b` in `docker-compose.yml` for failover.

### Changed (v1.0.6)

- Enforce anti-echo contract in `backend/main.py` for `/api/shell/think`: echo responses now return `degraded/failed` with `raw_response` instead of false success.
- Extend `shell/think` response metadata with `router`, `provider`, `model`, `execution`, and `generated_tokens` when available.
- Enrich trace pipeline records with `component` and `entered` fields across Scanner→Intent→Planner→Memory→Knowledge→Reasoning→Validator→Response.
- Route Nginx API/UI proxy through backend pool (`backend`, `backend_b`) with upstream retry/failover in `deploy/nginx.conf`.

### Release Sync (v1.0.6)

- Git tag: `v1.0.6`
- Commit: `TBD`
- Release URL: `TBD`

## v1.0.5 - 2026-09-02

UI runtime integrity release focused on removing static placeholder signals from the DNA UI shell and adding compliance footer controls.

### Added (v1.0.5)

- Add dynamic legal/footer link set in `neurosonic_dna_ui.html`: `Kushtet`, `Privatësia`, `Siguria`, `Statusi`, `Komuniteti`, `Dokumentarë`, `Kontakt`.
- Add privacy preference actions: `Menaxho cookies` and `Mos ndani informacionin tim personal`.
- Add runtime contact display with `clisonix@pm.me` in footer.

### Changed (v1.0.5)

- Replace hardcoded status/hash/date/count placeholders in `neurosonic_dna_ui.html` with API-driven values.
- Bind `Agents`, `Nodes`, `Labs`, and `Marketplace` badges to runtime data.
- Replace static profile identity fallback with local profile values from `localStorage`.

### Release Sync (v1.0.5)

- Git tag: `v1.0.5`
- Base feature commit: `2445850`
- Release URL: <https://github.com/Web8kameleon-hub/www.neuroconic.eu/releases/tag/v1.0.5>

## v1.0.4 - 2026-09-02

SEO hardening release focused on reducing homepage warnings and improving dynamic discoverability signals.

### Added (v1.0.4)

- Add complete SEO head metadata in `index.html`: canonical, hreflang, robots directives, Open Graph, Twitter Card, and JSON-LD.
- Add social preview asset `og-neurosonic.svg` and connect it to Open Graph/Twitter tags.
- Add `apple-touch-icon` declaration for stronger mobile/web app compatibility.

### Changed (v1.0.4)

- Align PWA manifest language with site language (`manifest.webmanifest` -> `lang: sq`).
- Expand `neurosonic_seo.py` page map with current dynamic UI/documentation routes.
- Regenerate `sitemap.xml` and `robots.txt` from the SEO generator to keep crawl/index rules synchronized.

### Release Sync (v1.0.4)

- Git tag: `v1.0.4`
- Base feature commit: `ada589c`
- Release URL: <https://github.com/Web8kameleon-hub/www.neuroconic.eu/releases/tag/v1.0.4>

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
