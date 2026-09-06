# Release Workflow

## Automated Flow (current)

Every push to `main` runs `.github/workflows/auto-release.yml`, which
invokes `scripts/release/auto_release.py`:

1. Collect real commit subjects since the last tag (`git log`).
2. Run the real validation suite: NO FAKE Police, OS-CLX Policy Guard,
   Repo Integrity Guard, Routes History Guard, Architecture Tests,
   `pytest -q`, `docker compose config`, `py_compile`.
3. If any check fails: abort. No version bump, no changelog entry, no
   release note, no tag, no GitHub Release. Nothing is fabricated.
4. If all checks pass: bump the patch version everywhere
   (`__init__.py`, `src/__init__.py`, `pyproject.toml`,
   `packages/npm/neurosonic-shell/package.json`, `backend/main.py`),
   prepend a `CHANGELOG.md` entry, write
   `docs/releases/vX.Y.Z.md`, commit, tag, push, and publish the
   GitHub Release — all from the same real data gathered in step 1-2.

No commit message keywords are required to trigger this; it runs on
every push to `main`. The only exception is a bot's own
`chore(release): ...` commits, which are skipped to avoid a release
bumping itself.

### Manual override / exceptions

- **Incident log** (`docs/production/evidence/incident_log.md`) is
  intentionally **not** auto-written — root-cause attribution needs
  human/agent judgment. Add incident rows by hand when a release fixes
  a real production incident.
- **Benchmarks** are intentionally **not** re-run automatically on every
  push (cost/time). Run `scripts/benchmark_compare.py` manually when a
  performance-sensitive change needs fresh evidence, and update
  `docs/production/evidence/benchmark_compare_latest.md` separately.
- To skip an automatic release for a specific push (e.g. a trivial
  typo fix), there is currently no opt-out flag; every push that changes
  `main` and passes validation is released. If this becomes noisy,
  extend `scripts/release/auto_release.py` with an explicit
  `[skip release]` commit-message check.

## Legacy Manual Flow (fallback if automation is disabled)

1. Finalize code + tests
2. Update `CHANGELOG.md`
3. Commit to `main`
4. Push to `origin`
5. Create semantic tag (`vX.Y.Z`)
6. Publish GitHub release notes

## Minimum Release Checklist

- [ ] Working tree clean
- [ ] Focused tests passed
- [ ] Changelog includes new version
- [ ] Tag points to intended commit
- [ ] Release URL verified

## Rollback Rule

Nëse release ka regresion kritik:

- krijo hotfix branch,
- rregullo root cause,
- publiko patch release të ri.
