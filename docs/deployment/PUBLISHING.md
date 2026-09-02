# Publishing Guide (PyPI, npm, crates)

This guide prepares and publishes Neurosonic shell packages across Python, Node.js, and Rust registries.

## 1) PyPI (`neurosonic`)

Build artifacts:

```bash
python -m pip install --upgrade build twine
python -m build
python -m twine check dist/*
```

Publish:

```bash
python -m twine upload dist/*
```

New CLI command included:

- `neurosonic-shell`

## 2) npm (`@web8kameleon-hub/neurosonic-shell`)

Package folder:

- `packages/npm/neurosonic-shell`

Validate and publish:

```bash
cd packages/npm/neurosonic-shell
npm pack --dry-run
npm publish --access public
```

## 3) crates.io (`neurosonic-shell`)

Package folder:

- `packages/crates/neurosonic-shell`

Validate and publish:

```bash
cd packages/crates/neurosonic-shell
cargo check
cargo package
cargo publish
```

## 4) Web8kameleon Hub Repository Linking

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
