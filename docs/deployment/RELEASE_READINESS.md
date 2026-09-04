# Release Readiness Runbook

This runbook prepares evidence for a release; it does not create a Git tag,
push a branch, publish a package, or deploy a service.

## Repository gates

Run the deterministic checks before any release decision:

```bash
python scripts/release_readiness.py --run-tests --output logs/release-readiness/latest.json
```

`ready: true` requires the complete test suite and live evidence. Running the
script without `--run-tests` or `--base-url` is intentionally not release-ready.
It is not a substitute for production approval.

## Live evidence

Start the intended backend, then run the same checks against its actual URL:

```bash
python scripts/release_readiness.py --run-tests --base-url http://127.0.0.1:8000 --output logs/release-readiness/latest.json
python scripts/benchmark_first.py --base-url http://127.0.0.1:8000 --profile quick --pretty
python scripts/benchmark_first.py --base-url http://127.0.0.1:8000 --profile quick --pretty
python scripts/benchmark_compare.py --pretty
```

The two benchmark runs must use the same profile and comparable hardware. The
benchmark records HTTP responses from the running backend; it intentionally
fails if the backend is unavailable or a scenario contract does not hold.

## Remaining approval steps

After readiness is green, review the release checklist, inspect `git status`,
commit the intended files, and choose the version/tag. Those actions remain an
explicit maintainer decision.
