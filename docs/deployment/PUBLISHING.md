# Publishing Guide (PyPI, npm, crates, Android TWA)

This guide prepares and publishes Neurosonic packages across Python, Node.js,
Rust, and Android.

## Automated publishing (current)

`.github/workflows/auto-release.yml` runs on every push to `main`:

1. `auto-release` job bumps the patch version, updates `CHANGELOG.md`,
   writes `docs/releases/vX.Y.Z.md`, tags, and publishes the GitHub Release
   -- but only if every real validation check passes (see
   `docs/wiki/Release-Workflow.md`).
2. `publish-packages` job then builds and publishes to PyPI, npm, and
   crates.io from that exact tagged commit -- **but only for registries
   that have a configured secret**. Each registry is checked independently
   and skipped (with a `::warning::` and a step summary line) if its
   secret is missing, exactly like the `DEPLOY_HOST`/`DEPLOY_SSH_KEY` check
   in `.github/workflows/autodeploy.yml`. Nothing is silently claimed as
   published if it wasn't.

Required repository secrets to enable each registry (Settings -> Secrets
and variables -> Actions):

| Registry | Secret | Notes |
| --- | --- | --- |
| PyPI | `PYPI_API_TOKEN` | API token scoped to the `neurosonic` project (or account-wide). Used as `TWINE_PASSWORD` with `TWINE_USERNAME=__token__`. |
| npm | `NPM_TOKEN` | Automation token with publish access to `@web8kameleon-hub/neurosonic-shell`. |
| crates.io | `CARGO_REGISTRY_TOKEN` | Token from <https://crates.io/settings/tokens>, scoped to `neurosonic-shell`. |

Until these secrets are added, `publish-packages` still runs (build +
`twine check` / `cargo package` / `npm pack` equivalents happen implicitly
via the publish commands' own validation) but each actual upload step is
skipped.

## Manual publishing (fallback / one-off)

### 1) PyPI (`neurosonic`)

```bash
python -m pip install --upgrade build twine
python -m build
python -m twine check dist/*
python -m twine upload dist/*
```

Console scripts included: `neurosonic`, `neurosonic-dna`,
`neurosonic-no-fake-police`, `neurosonic-shell`. All four are backed by
real top-level modules declared via `[tool.setuptools] py-modules` in
`pyproject.toml` -- verify with `python -m zipfile -l dist/*.whl` that
`neurosonic.py`, `neurosonic_core.py`, `neurosonic_no_fake_police.py`, and
`neurosonic_shell.py` are all present before publishing; a package missing
any of them would ship broken entry points.

### 2) npm (`@web8kameleon-hub/neurosonic-shell`)

```bash
cd packages/npm/neurosonic-shell
npm pack --dry-run
npm publish --access public
```

### 3) crates.io (`neurosonic-shell`)

```bash
cd packages/crates/neurosonic-shell
cargo check
cargo package
cargo publish
```

### 4) Android TWA (`eu.neurosonic.app`)

Not published through a registry -- distributed via Google Play. See
`packages/android/neurosonic-twa/README.md` for the full build, signing,
Digital Asset Links, and Play Store submission process. Summary:

```powershell
cd scripts/android
npm install
node generate-twa.mjs          # regenerate the Gradle project from manifest.webmanifest
cd ../../packages/android/neurosonic-twa
.\gradlew.bat bundleRelease    # requires a release keystore, see the package README
```

## 5) Web8kameleon Hub Repository Linking

Generate a live repository index from GitHub org `Web8kameleon-hub`:

```powershell
pwsh -File scripts/sync_web8kameleon_repos.ps1
```

Optional private org access:

```powershell
$env:GITHUB_TOKEN = "<github-token>"
pwsh -File scripts/sync_web8kameleon_repos.ps1
```

Generated files:

- `docs/community/WEB8KAMELEON_REPOS.md`
- `docs/community/web8kameleon_repos.json`

Use these artifacts in `neurosonic.eu` pages/API to expose all repos under the same hub.
