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

### Required setup: `RELEASE_PAT` (branch protection)

`main` is protected by a repository ruleset that blocks direct pushes
except from explicit bypass actors (currently the `LedjanAhmati` and
`Web8kameleon-hub` user accounts). GitHub's default per-workflow
`GITHUB_TOKEN` authors as the `github-actions[bot]` **Integration**
actor, and **Integration bypass actors are only supported for
repositories owned by a GitHub organization** — this repo is owned by a
personal account, so that route is not available
(`gh api .../rulesets` returns `"Actor GitHub Actions integration must
be part of the ruleset source or owner organization"`).

Because of this, the `auto-release` job needs a **Personal Access
Token (PAT)** stored as the `RELEASE_PAT` repository secret, created by
one of the bypass-listed accounts:

1. On GitHub, go to **Settings → Developer settings → Personal access
   tokens** (either "Fine-grained tokens" or "Tokens (classic)").
2. Create a token as `LedjanAhmati` or `Web8kameleon-hub`:
   - Fine-grained: scope it to this repository only, with **Contents:
     Read and write** permission (and **Metadata: Read-only**, which is
     required automatically).
   - Classic: use the `repo` scope.
3. Set an expiration and store the token securely; GitHub will not show
   it again.
4. Add it as a repository secret:
   `gh secret set RELEASE_PAT --repo Web8kameleon-hub/www.neuroconic.eu`
   (paste the token when prompted), or via
   **Settings → Secrets and variables → Actions → New repository secret**.

Until `RELEASE_PAT` is set, `auto-release` still runs every real
validation check and reports pass/fail honestly, but **skips** the
commit/tag/push/GitHub-Release steps (and the downstream
`publish-packages` job, which depends on the tag existing) rather than
failing with a confusing `GH013` push-rejection error. Check the
workflow run's step summary — it will say "NOT PUBLISHED" and point
back to this section when the PAT is missing.

If `main`'s branch protection is ever removed or changed to allow the
`github-actions[bot]` Integration through some other mechanism, the
workflow falls back to the default `GITHUB_TOKEN` automatically
(`token: ${{ secrets.RELEASE_PAT || github.token }}`), so `RELEASE_PAT`
can be safely removed at that point without editing the workflow file.

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
