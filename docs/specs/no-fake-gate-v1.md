# No-Fake Gate Rules v1

Specifikim i ekzekutueshëm për gate-in `Zero Fake` në runtime dhe CI.

## Objective

Bllokon pretendimet pa prova dhe modelet fake në kod/response:

- no mock/stub/simulation
- no placeholder runtime behavior
- no hardcoded metrics pa burim real
- no echo-as-success në reasoning flow

## Gate Surfaces

1. **Static Gate (code scan)**: para merge/deploy.
2. **Runtime Gate (response validation)**: para se API të kthejë `success=true`.
3. **Release Gate (tag/publish)**: kërkon prova të ekzekutimit real.

## Rule Set

## NF001 No Mock Imports

- **Block**: `unittest.mock`, `MagicMock`, `mock()`, `jest.fn`, `Mockito`, `sinon.stub`
- **Scope**: `src`, `backend`, `neurosonic*.py`, test policy exceptions sipas whitelist
- **Severity**: `critical`

## NF002 No Simulation Functions

- **Block patterns**: `_simulate`, `simulate_`, `fake_`, `stub_`, `emulate_`
- **Severity**: `high`

## NF003 No Placeholder Runtime

- **Block patterns**: `TODO`, `FIXME`, `NotImplemented`, `return {}`, `return None` në rrugë runtime kritike
- **Severity**: `high`

## NF004 No Hardcoded Trust Metrics

- **Block examples**:
  - `confidence = 0.99` pa llogaritje
  - `status = "completed"` pa verifikim
- **Severity**: `high`

## NF005 Anti-Echo Reasoning

- Nëse `normalized_output == normalized_prompt` ose output bosh:
  - response duhet të jetë `success=false`
  - `status=degraded|failed`
- **Severity**: `critical`

## NF006 Source and Integrity Trace Required

- Për rrugët reasoning:
  - kërkohet `trace_id`, `input_hash`, `output_hash`
  - `verification.reasoning_validated` duhet të jetë true vetëm me output të vlefshëm
- **Severity**: `critical`

## NF007 Plugin Security Gates

- Block plugin addresses me private/local host, invalid scheme, ose sensitive metadata keys.
- **Severity**: `critical`

## Decision Matrix

- Çdo `critical` -> `FAIL` (exit code 1)
- `high` >= 1 -> `FAIL`
- `medium` only -> `WARN` (exit code 0, por annotated)

## Finding JSON Contract

```json
{
  "gate_version": "1.0",
  "status": "fail",
  "summary": {
    "critical": 1,
    "high": 2,
    "medium": 0,
    "low": 0
  },
  "findings": [
    {
      "rule_id": "NF005",
      "severity": "critical",
      "file": "backend/main.py",
      "line": 742,
      "symbol": "shell_think",
      "message": "Echo response detected and returned as success.",
      "evidence": "output==prompt",
      "recommendation": "Return degraded/failed and clear user-facing response field."
    }
  ],
  "generated_at": "2026-09-02T19:40:00Z"
}
```

## CI Contract

Minimal gate pipeline:

```yaml
name: Zero Fake Gate
on: [push, pull_request]
jobs:
  no-fake-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Run No-Fake Gate
        run: python neurosonic_no_fake_police.py --ci
```

## Runtime Integration Points

- `backend/main.py`:
  - `/api/shell/think` anti-echo and verification gate
  - UI plugin attach security gate
- `neurosonic_ui_designer.py`:
  - export path sandbox

## Exit Codes

- `0`: pass
- `1`: fail (deploy blocked)
- `2`: execution error in gate engine

## Acceptance Criteria

- PR nuk merge-ohet nëse gate status = `fail`.
- Release tag nuk publikohet pa artefakt gate pass.
- API nuk raporton `success=true` për reasoning output që dështon NF005/NF006.
