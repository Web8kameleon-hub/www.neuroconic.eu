# 🧠 NEUROSONIC / CLISONIX TRINITY+ASI

## Zero Dependencies • Zero Fake • Zero Noise • Absolute Independence

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-success?style=flat-square)](./README.sq.md)
[![No Fake](https://img.shields.io/badge/NO%20FAKE-PASSING-ff69b4?style=flat-square)](NO_FAKE_POLICY.md)
[![Sovereign AI](https://img.shields.io/badge/Sovran-AI-8b5cf6?style=flat-square)](./docs/Architecture.md)

---

## 📋 Përshkrimi

Neurosonic është një **platformë AI e pavarur, 1000% sovrane**, e ndërtuar me **zero varësi nga jashtë**. Përdor vetëm Python standard library - asnjë pip install, asnjë npm, asnjë apt-get.

### Krijues: Ledjan Ahmati

---

## 🧩 Përbërësit Kryesorë

| Përbërësi | Përshkrimi |
| --------- | ---------- |
| 🧠 **CLX Kernel** | Runtime kryesor, planifikues i burimeve |
| 🧬 **HVO Memory** | 6 lloje memorie (Horizontal, Vertical, Orbital, Resonance, Film, Stigma) |
| 🔐 **Auth i Brendshëm** | Autentifikim pa OAuth |
| 💾 **NodeDB Fluid** | Database që përshtatet |
| 🧠 **Tubacioni i Mendimit** | 11 hapa (Scanner → Printer) |
| 🤖 **Shoqëria e Agjentëve** | Research, Shtet, Siguri |
| 📡 **SSE Streaming** | Transmetim i shpejtë |
| 🌊 **Tide Engine** | Batica/Zbatica |
| 🛡️ **Siguria** | Zero Trust, DDoS, Enkriptim |
| 🔢 **Algjebra** | 61 shtresa me alfabet shqip/grek |
| 💰 **Ekonomia e Brendshme** | Wallet, Licencë, Faturim |
| 🚓 **NO FAKE Police** | Zbatues i pastërtisë |

---

## 🚀 Ekzekutimi i Menjëhershëm

```bash
git clone https://github.com/LedjanAhmati/www.neurosonic.eu
cd www.neurosonic.eu
python neurosonic.py
```

**Asnjë instalim i jashtëm. Funksionon menjëherë.**

## 🛠️ Rikuperimi i Nisjes (Popup + Auto-clean Ports)

Nëse një instancë e vjetër mban portet (`8080`, `8000`, `5500`),
launcher-i kryesor i pastron automatikisht para nisjes së popup-ve.

```powershell
pwsh -File .\start_neurosonic.ps1
```

Çfarë ndodh automatikisht:

- Lirohen portet `8080` (Lightning SPP), `8000` (Backend), `5500` (Frontend)
- Hapet nga një dritare `pwsh` për secilin shërbim
- Hapet dashboard-i në `http://localhost:8000/neurosonic_dashboard.html`

Nëse `8080` mbetet i zënë, `scripts/popup_lightning.ps1` jep diagnostikë të qartë
me PID/ProcessName dhe shmang traceback-e të paqarta.

---

## 🗺️ Wiki, Stepstones & Vlerësime

- Wiki Home: `docs/wiki/Home.md`
- Stepstones Roadmap: `docs/STEPSTONES.md`
- Framework i Vlerësimit: `docs/EVALUATIONS.md`
- Workflow i Release-it: `docs/wiki/Release-Workflow.md`

---

## ⚖ë Kushtetuta (5 Shtyllat)

1. **SOVRANITETI** - Zero varësi nga shitës, punon offline
2. **E VËRTETA** - Zero fake, gjithçka e verifikueshme
3. **PRIVATËSIA** - Të dhënat e përdoruesit janë pronë e tij
4. **ARKITEKTURA** - Modular, i shpërndarë, HVO memory
5. **QEVERISJA** - Kushtetuta mbi çdo modul

---

## 🌐 Hostimi Production

Për hostim përdoret Docker Compose me Nginx, FastAPI dhe Lightning SPP si
shërbime të ndara:

```bash
cp .env.example .env
docker compose config
docker compose build --pull
docker compose up -d
```

Lexo [udhëzuesin e hostimit](docs/deployment/HOSTING.md),
[runbook-un operacional](docs/deployment/OPERATIONS.md),
[sigurinë e hostimit](docs/deployment/SECURITY.md) dhe
[checklist-in e release-it](docs/deployment/RELEASE_CHECKLIST.md).

## 🔬 Testet

```bash
python test_architecture.py
```

---

## 🚓 NO FAKE Police

```bash
python neurosonic_no_fake_police.py --ci  # CI kontroll
python neurosonic_no_fake_police.py --cd  # CD kontroll (bllokon deploy)
```

---

## 🌍 Lidhjet

- 🌐 [neurosonic.eu](https://www.neurosonic.eu)
- 🐙 [GitHub](https://github.com/LedjanAhmati/www.neurosonic.eu)
- 📖 [Dokumentacioni](docs/Architecture.md)
- 🗺️ [Wiki Home](docs/wiki/Home.md)
- 🧭 [Stepstones](docs/STEPSTONES.md)
- 📊 [Vlerësime](docs/EVALUATIONS.md)

---

## NEUROSONIC / CLISONIX TRINITY+ASI v1.0

> "Kodi që nuk është real, nuk ekzekutohet."
