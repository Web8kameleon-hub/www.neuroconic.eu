# 🤝 Contributing to Neurosonic / Clisonix Trinity+ASI

First off, thank you for considering contributing to Neurosonic!

## 📜 Neurosonic Constitution

By contributing, you agree to abide by the [Neurosonic Constitution](docs/Constitution.md):

1. **SOVEREIGNTY** - No external dependencies
2. **TRUTH** - No fake, no hallucination
3. **PRIVACY** - User data is user property
4. **ARCHITECTURE** - Modular, distributed, HVO
5. **GOVERNANCE** - Constitution above all

## 🚫 NO FAKE Policy

All code must pass [NO FAKE POLICE](NO_FAKE_POLICY.md):

- Zero mock libraries (unittest.mock, MagicMock, Mockito, sinon, jest.fn)
- Zero simulation functions (def simulate, def _fake_, def _stub)
- Zero placeholders (NotImplementedError as placeholder)
- Zero hardcoded values in real code
- CD is BLOCKED if violations exist

R&D zhvillim lejohet vetëm për koncepte/drafte/protokolle/formula të reja në
`docs/`, `samples/`, `examples/`, me etiketë të qartë `EXPERIMENTAL` ose
`DRAFT`. Këto nuk duhet të futen si runtime production në `src/` ose `backend/`.

## 🔧 Development Setup

```bash
# Clone the repo
git clone https://github.com/LedjanAhmati/www.neuroconic.eu
cd www.neuroconic.eu

# No pip install needed! Zero dependencies.
python neurosonic.py
```

## 🧪 Running Tests

```bash
# Run all architecture tests
python test_architecture.py

# Run NO FAKE police
python neurosonic_no_fake_police.py --ci

# Run benchmark contract tests
python -m pytest -q tests/test_benchmark_first.py tests/test_benchmark_edge_cases.py

# Enforce minimum test inventory
python scripts/assert_min_test_count.py --minimum 64
```

## 🌊 Single-Branch Production Rule

Ky repo ndjek **main-only production flow**:

- Vetëm dega `main` konsiderohet dega e zhvilluar dhe e deploy-ueshme.
- Nuk mbahen degë dekorative/sterile si strategji standarde release.
- CI/CD dhe guardrails targetojnë `main` për konsistencë prodhimi.
- Çdo ndryshim duhet të përfundojë i testuar me benchmark contract tests.

## 📁 Project Structure

```text
neurosonic.eu/
├── docs/           - Constitution, CUDM, Architecture
├── neurosonic.py   - Main entry
├── neurosonic_*.py - Core modules (DNA, Genome, Evolution, etc.)
├── test_*.py       - Tests
└── NO_FAKE_POLICY.md - NO FAKE enforcement
```

## 🧬 Contribution Workflow

1. Fork the repo
2. Sync with `main`
3. Make changes (zero dependencies only!)
4. Run `python neurosonic_no_fake_police.py --ci` (must pass)
5. Run `python test_architecture.py` (must pass)
6. Run `python -m pytest -q tests/test_benchmark_first.py tests/test_benchmark_edge_cases.py` (must pass)
7. Commit (`git commit -m 'Your change'`)
8. Push to `main` and verify CI green

## ✅ Pull Request Checklist

- [ ] Code follows Neurosonic Constitution
- [ ] NO FAKE POLICE passes (zero violations)
- [ ] All architecture tests pass
- [ ] Zero external dependencies added
- [ ] Documentation updated
- [ ] No hardcoded values
- [ ] Every response has source verification

## 📝 Code Style

- Use type hints
- Keep functions under 50 lines
- Document every function with docstrings
- Use `hashlib.sha256` for verification
- Log every action for audit trail

## ❓ Questions?

Open a [GitHub Discussion](https://github.com/LedjanAhmati/www.neuroconic.eu/discussions)

---

**Neurosonic / Clisonix Trinity+ASI v1.0**
_Kodi që nuk është real, nuk ekzekutohet._
