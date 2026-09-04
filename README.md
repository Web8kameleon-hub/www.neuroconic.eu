# 🧠 NEUROSONIC / CLISONIX TRINITY+ASI

> Evidence-first AI platform with optional runtime profiles

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Neurosonic-green?style=flat-square)](LICENSE)
[![Core Stdlib](https://img.shields.io/badge/core-stdlib%20mode-success?style=flat-square)](PUBLIC_USAGE.md)
[![No Fake](https://img.shields.io/badge/NO%20FAKE-PASSING-ff69b4?style=flat-square)](NO_FAKE_POLICY.md)
[![GitHub Stars](https://img.shields.io/github/stars/LedjanAhmati/www.neurosonic.eu?style=flat-square&logo=github)](https://github.com/LedjanAhmati/www.neurosonic.eu)
[![GitHub Issues](https://img.shields.io/github/issues/LedjanAhmati/www.neurosonic.eu?style=flat-square&logo=github)](https://github.com/LedjanAhmati/www.neurosonic.eu/issues)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/LedjanAhmati/www.neurosonic.eu?style=flat-square&logo=github)](https://github.com/LedjanAhmati/www.neurosonic.eu)
[![Build](https://img.shields.io/badge/build-passing-brightgreen?style=flat-square)](docs/deployment/RELEASE_CHECKLIST.md)
[![Guardrails CI](https://img.shields.io/badge/guardrails-CI%20enforced-0ea5e9?style=flat-square)](https://github.com/Web8kameleon-hub/www.neuroconic.eu/actions/workflows/ci.yml)
[![Sovereign AI](https://img.shields.io/badge/Sovereign-AI-8b5cf6?style=flat-square)](docs/Constitution.md)

---

## 📋 Përshkrimi

Neurosonic është një platformë AI me dy mënyra përdorimi:

- **Core mode (stdlib-first)**: komponentët bazë që mund të ekzekutohen pa profile të jashtme.
- **Backend/dev/public profiles**: aktivizohen me `requirements*.txt` ose extras te `pyproject.toml`.

Pretendimet në këtë README janë të lidhura me artefakte testimi, benchmark dhe guardrails që gjenden në repo.

### 🔑 Fjalë Kyçe

`neurosonic` `clisonix` `trinity-asi` `sovereign-ai` `zero-dependencies` `hvo-memory` `multi-agent` `distributed-computing` `no-fake-ai` `python`

---

## 📑 Table of Contents

- [🧠 NEUROSONIC / CLISONIX TRINITY+ASI](#-neurosonic--clisonix-trinityasi)
  - [📋 Përshkrimi](#-përshkrimi)
    - [🔑 Fjalë Kyçe](#-fjalë-kyçe)
  - [📑 Table of Contents](#-table-of-contents)
  - [🧩 Komponentët Kryesorë](#-komponentët-kryesorë)
  - [🚀 Ekzekutimi i Menjëhershëm](#-ekzekutimi-i-menjëhershëm)
  - [🛠️ Startup Recovery (Popup + Auto-clean Ports)](#️-startup-recovery-popup--auto-clean-ports)
  - [🗺️ Wiki, Stepstones \& Evaluations](#️-wiki-stepstones--evaluations)
  - [📁 Struktura e Projektit](#-struktura-e-projektit)
  - [⚖️ Kushtetuta (5 Shtyllat)](#️-kushtetuta-5-shtyllat)
  - [🌐 Production Hosting](#-production-hosting)
  - [📦 Public Installation Packs](#-public-installation-packs)
  - [⚡ First Benchmark (baseline + tuning + edge cases)](#-first-benchmark-baseline--tuning--edge-cases)
  - [📦 Publishing (PyPI + npm + crates)](#-publishing-pypi--npm--crates)
  - [🧭 OS-CLX Policy (lightweight) + Cross-Repo Acceleration](#-os-clx-policy-lightweight--cross-repo-acceleration)
  - [📈 Production Evidence Pack](#-production-evidence-pack)
  - [📡 Full Observability Pack](#-full-observability-pack)
  - [📊 Comparative Benchmark Evidence](#-comparative-benchmark-evidence)
  - [🧯 Formal Threat Modeling (STRIDE)](#-formal-threat-modeling-stride)
  - [🌍 External Benchmark Evidence](#-external-benchmark-evidence)
  - [🧱 Structure Consolidation Plan](#-structure-consolidation-plan)
  - [🔬 Testet](#-testet)
  - [🚓 NO FAKE Police](#-no-fake-police)
  - [🤝 Kontribuimi](#-kontribuimi)
  - [📜 Licenca](#-licenca)
  - [🌍 Lidhjet](#-lidhjet)
  - [NEUROSONIC / CLISONIX TRINITY+ASI v1.0](#neurosonic--clisonix-trinityasi-v10)

---

## 🧩 Komponentët Kryesorë

| Komponenti | Përshkrimi |
| ---------- | ---------- |
| 🧠 **CLX Kernel** | Runtime kryesor, scheduler i burimeve |
| 🧬 **HVO Memory** | 6 lloje memorie (H, V, O, R, F, S) |
| 🔐 **Internal Auth** | Autentifikim i brendshëm pa OAuth |
| 💾 **NodeDB Fluid** | Database adaptiv |
| 🧠 **Thinking Pipeline** | 11 hapa mendimi |
| 🤖 **Agent Society** | Research, Country, Security Agents |
| 📡 **SSE Streaming** | Transmetim me shpejtësi |
| 🌊 **Tide Engine** | Batica/Zbatica |
| 🛡️ **Security Engine** | Zero Trust, DDoS, Encryption |
| 🔢 **Algebra Engine** | 61 shtresa me alfabet grek/shqip |
| 💰 **Internal Economy** | Wallet, License, Billing |
| 📋 **Audit Logger** | Logje të pandryshueshme |
| 🚓 **NO FAKE Police** | CI/CD enforcement |

---

## 🚀 Ekzekutimi i Menjëhershëm

```bash
# Clone
git clone https://github.com/LedjanAhmati/www.neurosonic.eu
cd www.neurosonic.eu

# Core shell mode (stdlib-first)
python neurosonic.py

# Backend/API profile
pip install -r requirements.txt
python -m backend.main
```

## 🛠️ Startup Recovery (Popup + Auto-clean Ports)

Nëse një instancë e vjetër mban portet (`8080`, `8000`, `5500`),
launcher-i kryesor tani i pastron automatikisht para nisjes së popup-ve.

```powershell
pwsh -File .\start_neurosonic.ps1
```

Çfarë ndodh automatikisht:

- Lirohen portet `8080` (Lightning SPP), `8000` (Backend), `5500` (Frontend)
- Hapet nga një dritare `pwsh` për secilin shërbim
- Hapet dashboard-i në `http://localhost:8000/neurosonic_dashboard.html`

Nëse `8080` është ende i zënë, `scripts/popup_lightning.ps1` tani jep
diagnostikë të qartë me PID/ProcessName dhe nuk bie me traceback të paqartë.

---

## 🗺️ Wiki, Stepstones & Evaluations

- Wiki Home: `docs/wiki/Home.md`
- Stepstones Roadmap: `docs/STEPSTONES.md`
- Evaluation Framework: `docs/EVALUATIONS.md`
- Release Workflow (wiki): `docs/wiki/Release-Workflow.md`

---

## 📁 Struktura e Projektit

```text
neurosonic.eu/
├── docs/                    # Dokumentacioni
│   ├── Constitution.md      # Kushtetuta (5 shtyllat)
│   ├── CUDM.md              # Unified Data Model
│   └── Architecture.md      # 12 shtyllat e arkitekturës
├── src/                     # Source code
│   ├── kernel/              # Runtime, Memory, Auth, NodeDB
│   ├── ai/                  # CLX-LLM, CLX.I, Reasoning
│   ├── agents/              # Research, Country, Protocol
│   ├── network/             # Mesh, SSE, Protocols
│   ├── tide/                # Tide Engine
│   ├── governance/          # Policies, Compliance
│   ├── security/            # Encryption, DDoS
│   ├── api/                 # Internal & Public API
│   ├── economy/             # Wallet, Billing, License
│   └── performance/         # Noise Filter, Heartbeat
├── neurosonic.py            # Bootstrap kryesor
├── neurosonic_dna.py        # DNA - I pandryshueshëm
├── neurosonic_genome.py     # GENOME - Zgjerohet
├── neurosonic_compatibility.py  # Compatibility Matrix
├── neurosonic_evolution.py  # Evolution Engine
├── neurosonic_no_fake_police.py # NO FAKE Police
├── neurosonic_lightning_bridge.py # Lightning SPP Bridge
├── test_architecture.py     # Testet e plota
├── NO_FAKE_POLICY.md        # Politika NO FAKE
├── CONTRIBUTING.md          # Udhëzime për kontribuim
├── sitemap.xml              # SEO sitemap
├── robots.txt               # SEO robots
└── index.html               # Web UI
```

---

## ⚖️ Kushtetuta (5 Shtyllat)

| Shtylla | Parimet |
| ------- | ------- |
| 🏛️ **SOVRANITETI** | Zero vendor lock-in, offline capable, internal auth |
| 🔍 **E VËRTETA** | Zero fake, hallucination, çdo gjë e verifikueshme |
| 🔒 **PRIVATËSIA** | User data = pronë e përdoruesit, encrypted |
| 🧩 **ARKITEKTURA** | Modular, distributed, HVO memory, CUDM |
| ⚖️ **QEVERISJA** | Constitution mbi çdo modul, human override |

---

## 🌐 Production Hosting

Production uses Docker Compose with separate Nginx, FastAPI, and Lightning SPP
services:

```bash
cp .env.example .env
docker compose config
docker compose build --pull
docker compose up -d
```

Read the [hosting guide](docs/deployment/HOSTING.md),
[operations runbook](docs/deployment/OPERATIONS.md),
[hosting security guide](docs/deployment/SECURITY.md), and
[release checklist](docs/deployment/RELEASE_CHECKLIST.md).

## 📦 Public Installation Packs

For large/public usage scenarios, use one of these profiles:

```bash
# Core project (zero extra deps)
python neurosonic.py

# Backend/API runtime deps
pip install -r requirements.txt

# Dev + tests
pip install -r requirements-dev.txt

# Or extras via pyproject
pip install .[backend]
pip install .[dev]
pip install .[public]
```

Public resources added for quick onboarding:

- `examples/basic_usage.py`
- `examples/lightning_bridge_sample.py`
- `samples/module_config_valid.json`
- `samples/module_config_invalid.json`
- `tests/test_public_samples.py`
- `tests/test_examples_smoke.py`

Run the public smoke suite:

```bash
pytest -q tests/test_public_samples.py tests/test_examples_smoke.py
```

## ⚡ First Benchmark (baseline + tuning + edge cases)

Run the initial benchmark harness:

```bash
python scripts/benchmark_first.py --base-url http://127.0.0.1:8000 --profile quick --pretty
```

Available tuning profiles:

- `quick` (fast local validation)
- `standard` (balanced signal)
- `stress` (high iteration pressure)

Useful overrides:

```bash
python scripts/benchmark_first.py --base-url http://127.0.0.1:8000 --profile standard --iterations 80 --warmup 10 --long-prompt-size 16384 --pretty
```

What it measures in one run:

- `/api/shell/think` success baseline
- `/api/shell/think` edge cases (empty prompt, echo response, long prompt)
- `/api/ui/plugins/{profile_id}` edge/security checks (private network, sensitive metadata)
- plugin attach success baseline

Output is written to `logs/benchmarks/live-benchmark-<timestamp>.json` with latency (`min`, `p50`, `p95`, `max`, `mean`, `stdev`), throughput (`rps`), and pass-rate per live scenario. The backend URL is required; unavailable services fail the run.

Kontrata për shell + NodeDB Fluid (anti-konflikt cross-language):

- `docs/governance/NODEDB_FLUID_SHELL_CONTRACT.md`

## 📦 Publishing (PyPI + npm + crates)

Multi-ecosystem publishing is now prepared:

- PyPI package and CLI entrypoint `neurosonic-shell`
- npm package `packages/npm/neurosonic-shell`
- Rust crate `packages/crates/neurosonic-shell`

Full commands and release flow are documented in:

- `docs/deployment/PUBLISHING.md`

To sync/link all repositories under `Web8kameleon-hub` for `neurosonic.eu`:

```powershell
pwsh -File scripts/sync_web8kameleon_repos.ps1
```

## 🧭 OS-CLX Policy (lightweight) + Cross-Repo Acceleration

Për të sjellë ide nga repo të tjera pa e rënduar këtë repo:

- Udhëzues: `docs/guides/OS_CLX_CROSS_REPO_ACCELERATION.md`
- Policy profile: `docs/governance/OS_CLX_POLICY_PROFILE.json`
- Guard script: `scripts/os_clx_policy_guard.py`

Run policy guard:

```bash
python scripts/os_clx_policy_guard.py
```

Strict mode (fail edhe për warnings):

```bash
python scripts/os_clx_policy_guard.py --strict
```

Guardrails të portuara nga OS-CLX (lightweight):

- `scripts/guardrails/repo_integrity_guard.py`
- `scripts/guardrails/routes_history_guard.py`
- `scripts/guardrails/compose.services.txt`

Run integrity + routes history guards:

```bash
python scripts/guardrails/repo_integrity_guard.py
python scripts/guardrails/routes_history_guard.py
```

Artefaktet e raportit gjenerohen te:

- `docs/production/canonical/repo_integrity_guard_report.json`
- `docs/production/canonical/routes_history_guard_report.json`

Immutable release manifest workflow:

- `.github/workflows/release-immutable.yml`
- Trigger: `git tag vX.Y.Z ; git push origin vX.Y.Z` ose manual `workflow_dispatch`

## 📈 Production Evidence Pack

Gjenero artefaktet bazë të evidencës (latency trend, availability trend, incident log, rollback drills):

```bash
python scripts/production_evidence_pack.py --pretty
```

Artefaktet ruhen te:

- `docs/production/evidence/latency_trend.json`
- `docs/production/evidence/availability_trend.json`
- `docs/production/evidence/incident_log.md`
- `docs/production/evidence/rollback_drills.md`

## 📡 Full Observability Pack

SLO dashboards, error budgets dhe tracing uniform janë formalizuar te:

- `docs/production/observability/SLO_DEFINITIONS.json`
- `docs/production/observability/SLO_DASHBOARD_GRAFANA.json`
- `docs/production/observability/ERROR_BUDGET_POLICY.md`
- `docs/production/observability/TRACING_UNIFORM_STANDARD.md`

Gjenero snapshot-in e SLO/error budget nga evidenca aktuale:

```bash
python scripts/observability_slo_snapshot.py --pretty
```

Valido tracing contract-in në endpoint real:

```bash
python scripts/trace_uniform_check.py --base-url http://127.0.0.1:8000
```

Artefaktet e observability ruhen te:

- `docs/production/evidence/slo_snapshot_latest.json`
- `docs/production/evidence/error_budget_status_latest.md`
- `docs/production/evidence/trace_uniform_check_latest.json`

## 📊 Comparative Benchmark Evidence

Krahason dy benchmark outputs reale dhe prodhon raport JSON + Markdown:

```bash
python scripts/benchmark_compare.py --pretty
```

Default behavior: përdor dy skedarët më të fundit te `logs/benchmarks/live-benchmark-*.json`.

Artefaktet ruhen te:

- `docs/production/evidence/benchmark_compare_latest.json`
- `docs/production/evidence/benchmark_compare_latest.md`

## 🧯 Formal Threat Modeling (STRIDE)

Threat model formal me assets, trust boundaries, STRIDE register dhe risk scoring:

- `docs/production/security/THREAT_MODEL_STRIDE.md`

## 🌍 External Benchmark Evidence

Referencat e benchmark-eve të jashtme dhe mapping-u me evidencën lokale:

- `docs/production/evidence/EXTERNAL_BENCHMARK_EVIDENCE.md`
- `docs/production/evidence/external_benchmark_evidence.json`

## 🧱 Structure Consolidation Plan

Për hartën aktuale të moduleve dhe planin e konsolidimit pa refaktor destruktiv, shih:

- `docs/guides/STRUCTURE_CONSOLIDATION_PLAN.md`

## 🔬 Testet

```bash
python test_architecture.py
```

Sistemi përfshin 13+ teste automatike që verifikojnë:

- ✅ Kushtetutën (DNA)
- ✅ HVO Memory (6 lloje)
- ✅ Internal Auth
- ✅ NodeDB Fluid
- ✅ Thinking Pipeline (11 hapa)
- ✅ Agent Society
- ✅ SSE Streaming
- ✅ Tide Engine
- ✅ Security (DDoS, Encryption)
- ✅ Algebra Engine (61 shtresa)
- ✅ Internal Economy
- ✅ Internal API
- ✅ Audit Logger

---

## 🚓 NO FAKE Police

```bash
# Run NO FAKE check
python neurosonic_no_fake_police.py

# CI mode (exit 1 on violations)
python neurosonic_no_fake_police.py --ci

# CD mode (block deploy on violations)
python neurosonic_no_fake_police.py --cd
```

Zbulon:

- ❌ Mock libraries (unittest.mock, MagicMock)
- ❌ Simulation functions (def simulate, def _fake_)
- ❌ Placeholders (NotImplementedError)
- ❌ Hardcoded values in real code

---

## 🤝 Kontribuimi

Shiko [CONTRIBUTING.md](CONTRIBUTING.md) për udhëzime të plota.

**Kushti kryesor**: Asnjë kod që nuk kalon NO FAKE Police nuk pranohet.

---

## 📜 Licenca

Neurosonic License - Shih [LICENSE](LICENSE) për detaje.

---

## 🌍 Lidhjet

- 🌐 [neurosonic.eu](https://www.neurosonic.eu)
- 🐙 [GitHub](https://github.com/LedjanAhmati/www.neurosonic.eu)
- 📖 [Dokumentacioni](docs/Architecture.md)
- 🧬 [Kushtetuta](docs/Constitution.md)
- 🗺️ [Wiki Home](docs/wiki/Home.md)
- 🧭 [Stepstones](docs/STEPSTONES.md)
- 📊 [Evaluations](docs/EVALUATIONS.md)

---

## NEUROSONIC / CLISONIX TRINITY+ASI v1.0

> "Jo një AI i vetëm. Por një ekosistem i shpërndarë, ku çdo pajisje bëhet një qendër mendimi."

> "Kodi që nuk është real, nuk ekzekutohet."
