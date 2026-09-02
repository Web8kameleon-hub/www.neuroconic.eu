# Public Usage Pack (Neurosonic)

Ky dokument përmbledh instalimin, testimin dhe shembujt për përdorim publik në shkallë.

## 1) Install Profiles

```bash
# Runtime backend/API profile
pip install -r requirements.txt

# Development + tests
pip install -r requirements-dev.txt

# Equivalent via pyproject extras
pip install .[backend]
pip install .[dev]
pip install .[public]
```

## 2) Public Examples

```bash
python examples/basic_usage.py
python examples/lightning_bridge_sample.py
```

## 3) Public Sample Configs

- `samples/module_config_valid.json`
- `samples/module_config_invalid.json`

## 4) Public Smoke Tests

```bash
pytest -q tests/test_public_samples.py tests/test_examples_smoke.py
```

## 5) Hosting Baseline

```bash
cp .env.example .env
docker compose config
docker compose build --pull
docker compose up -d
```

Hosting runbooks:

- `docs/deployment/HOSTING.md`
- `docs/deployment/OPERATIONS.md`
- `docs/deployment/SECURITY.md`
- `docs/deployment/RELEASE_CHECKLIST.md`
