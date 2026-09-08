#!/usr/bin/env python3
"""Automated release-cut pipeline.

Generates the version bump, CHANGELOG entry, and release note for a patch
release using ONLY real, locally-observed facts:

- commit subjects pulled from `git log` since the last tag (no invented
  "highlights" prose),
- validation results captured from actually running the same guardrails,
  tests, and compile checks used in CI.

If any real check fails, the script exits non-zero and writes NOTHING --
there is no "release documentation" for a release that did not actually
pass. This mirrors the NO FAKE / Zero Fake policy enforced elsewhere in
this repository.

Usage:
    python scripts/release/auto_release.py --dry-run   # print, don't write (default)
    python scripts/release/auto_release.py --write      # write files, no git ops
    python scripts/release/auto_release.py --print-version-only

The calling workflow is responsible for `git add/commit/tag/push` and
`gh release create` once this script exits 0.

Exit codes:
    0 - success (release files written, or dry-run/print-only completed)
    1 - one or more validation checks FAILED; nothing was written
    3 - no-op: no new commits since the last tag
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

ROOT = Path(__file__).resolve().parents[2]
REPO_URL = "https://github.com/Web8kameleon-hub/www.neuroconic.eu"

VERSION_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


@dataclass
class CheckResult:
    name: str
    status: str  # PASS | FAIL | SKIPPED
    detail: str


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def get_current_version() -> str:
    text = _read(ROOT / "__init__.py")
    match = re.search(r'__version__\s*=\s*"([^"]+)"', text)
    if not match:
        raise RuntimeError("Could not find __version__ in __init__.py")
    return match.group(1)


def bump_patch(version: str) -> str:
    match = VERSION_RE.match(version)
    if not match:
        raise RuntimeError(f"Version '{version}' is not X.Y.Z semver")
    major, minor, patch = (int(part) for part in match.groups())
    return f"{major}.{minor}.{patch + 1}"


def get_last_tag() -> Optional[str]:
    result = subprocess.run(
        ["git", "describe", "--tags", "--abbrev=0"],
        cwd=ROOT, capture_output=True, text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def get_commits_since(last_tag: Optional[str]) -> List[str]:
    range_spec = f"{last_tag}..HEAD" if last_tag else "HEAD"
    result = subprocess.run(
        ["git", "log", "--no-merges", "--pretty=format:%h %s", range_spec],
        cwd=ROOT, capture_output=True, text=True,
    )
    if result.returncode != 0:
        return []
    subjects = [line for line in result.stdout.splitlines() if line.strip()]
    # Never let a prior auto-release commit re-appear as a "highlight".
    return [s for s in subjects if "chore(release):" not in s]


def run_check(name: str, cmd: List[str], timeout: int = 900) -> CheckResult:
    exe = cmd[0]
    if exe != sys.executable and shutil.which(exe) is None:
        return CheckResult(name, "SKIPPED", f"'{exe}' not available on this runner")
    try:
        result = subprocess.run(
            cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout,
        )
    except Exception as exc:  # pragma: no cover - defensive
        return CheckResult(name, "FAIL", f"exception: {exc}")

    status = "PASS" if result.returncode == 0 else "FAIL"
    tail = (result.stdout + result.stderr).strip().splitlines()
    detail = "\n".join(tail[-8:]) if tail else "(no output)"
    return CheckResult(name, status, detail)


def run_all_checks() -> List[CheckResult]:
    py = sys.executable
    checks = [
        ("NO FAKE Police", [py, "neurosonic_no_fake_police.py", "--ci"]),
        ("OS-CLX Policy Guard", [py, "scripts/os_clx_policy_guard.py", "--strict"]),
        ("Repo Integrity Guard", [py, "scripts/guardrails/repo_integrity_guard.py"]),
        ("Routes History Guard", [py, "scripts/guardrails/routes_history_guard.py"]),
        ("Architecture Tests", [py, "test_architecture.py"]),
        ("Pytest", [py, "-m", "pytest", "-q"]),
        ("Docker Compose Config", ["docker", "compose", "-f", "docker-compose.yml", "config", "--quiet"]),
        ("Py Compile", [py, "-m", "py_compile", "__init__.py", "neurosonic.py",
                         "neurosonic_core.py", "backend/main.py", "src/__init__.py"]),
    ]
    return [run_check(name, cmd) for name, cmd in checks]


def bump_version_files(old: str, new: str) -> List[str]:
    """Rewrite every known version-bearing file. Returns list of touched paths.

    Validates every required file/pattern BEFORE writing any of them, so a
    single missing string aborts with nothing written (no partial bump).
    """
    simple_targets = [
        (ROOT / "__init__.py", [(f'__version__ = "{old}"', f'__version__ = "{new}"')]),
        (ROOT / "src" / "__init__.py", [(f'__version__ = "{old}"', f'__version__ = "{new}"')]),
        (ROOT / "pyproject.toml", [(f'version = "{old}"', f'version = "{new}"')]),
        (ROOT / "packages" / "npm" / "neurosonic-shell" / "package.json",
         [(f'"version": "{old}"', f'"version": "{new}"')]),
        (ROOT / "packages" / "crates" / "neurosonic-shell" / "Cargo.toml",
         [(f'version = "{old}"', f'version = "{new}"')]),
        (ROOT / "backend" / "main.py", [
            (f'version="{old}"', f'version="{new}"'),
            (f'"version": "{old}"', f'"version": "{new}"'),
            (f'"api_version": "{old}"', f'"api_version": "{new}"'),
        ]),
    ]

    # Cargo.lock pins the crate's own version alongside its dependency graph;
    # patch only the crate's self-entry (name = "neurosonic-shell" block),
    # not any dependency that happens to share the same version string.
    # Optional: only required if present and if it actually still has the
    # old version recorded (a fresh checkout always will, post-bump).
    cargo_lock = ROOT / "packages" / "crates" / "neurosonic-shell" / "Cargo.lock"
    cargo_lock_old_block = f'name = "neurosonic-shell"\nversion = "{old}"'
    cargo_lock_new_block = f'name = "neurosonic-shell"\nversion = "{new}"'
    bump_cargo_lock = cargo_lock.exists() and cargo_lock_old_block in _read(cargo_lock)

    # Pass 1: validate every required file/pattern exists. Raise before
    # writing anything if any expectation is not met.
    file_texts: dict[Path, str] = {}
    for path, replacements in simple_targets:
        text = _read(path)
        for old_str, _new_str in replacements:
            if old_str not in text:
                raise RuntimeError(f"Expected '{old_str}' not found in {path}")
        file_texts[path] = text

    # Pass 2: apply replacements and write, now that everything validated.
    touched: List[str] = []
    for path, replacements in simple_targets:
        text = file_texts[path]
        for old_str, new_str in replacements:
            text = text.replace(old_str, new_str, 1)
        _write(path, text)
        touched.append(str(path.relative_to(ROOT)))

    if bump_cargo_lock:
        text = _read(cargo_lock)
        _write(cargo_lock, text.replace(cargo_lock_old_block, cargo_lock_new_block, 1))
        touched.append(str(cargo_lock.relative_to(ROOT)))
    elif cargo_lock.exists():
        print(f"[auto-release] WARNING: could not find self-entry to bump in {cargo_lock}; "
              f"run 'cargo check' in packages/crates/neurosonic-shell manually.")

    return touched


def render_validation_table(results: List[CheckResult]) -> str:
    return "\n".join(f"- `{r.name}` -> **{r.status}**" for r in results)


def render_release_note(version: str, date: str, last_tag: Optional[str],
                         commits: List[str], results: List[CheckResult]) -> str:
    commit_lines = "\n".join(f"- `{c}`" for c in commits) or "- (no new commits recorded since last tag)"
    validation = render_validation_table(results)
    since = last_tag or "repository start"

    return f"""# Release {version}

Date: {date}

## Origin

This release note was generated automatically by
`scripts/release/auto_release.py` from real repository state:
commit subjects since `{since}` and the actual exit status of the checks
below. Nothing in this file is hand-written or inferred.

## Commits included

{commit_lines}

## Edge cases covered

- This release is only cut when every check in "Validation snapshot" is
  `PASS` (or `SKIPPED` because the tool is unavailable on the runner).
  A single `FAIL` blocks the version bump, changelog entry, tag, and
  GitHub Release for this push.
- Version strings are updated across all known files in one pass
  (`__init__.py`, `src/__init__.py`, `pyproject.toml`,
  `packages/npm/neurosonic-shell/package.json`,
  `packages/crates/neurosonic-shell/Cargo.toml`, `backend/main.py`); a
  missing expected string aborts the release instead of silently
  skipping a file.

## Validation snapshot

{validation}

## Benchmark

No benchmark suite is re-run automatically as part of this pipeline
(cost/time reasons). See
`docs/production/evidence/benchmark_compare_latest.md` for the latest
reference numbers; treat them as unchanged for this release unless a
separate benchmark run says otherwise.

## Incident record

Root-cause attribution requires human/agent judgment and is
intentionally **not** automated. If this release fixes a real
production incident, add a row to
`docs/production/evidence/incident_log.md` manually.

## Stepstone alignment

Per `docs/wiki/Operations-Stepstones.md`, Stepstone 4 (Release
Excellence) exit criteria for this release:

- Changelog updated: yes (`CHANGELOG.md`, this file) -- automatic.
- Semantic tag created: `v{version}` -- automatic.
- GitHub Release published: yes -- automatic.

## Tag + repository

- Tag: `v{version}`
- Repository: <{REPO_URL}>
"""


def render_changelog_entry(version: str, date: str, last_tag: Optional[str],
                            commits: List[str], results: List[CheckResult]) -> str:
    commit_lines = "\n".join(f"- `{c}`" for c in commits) or "- (no new commits recorded since last tag)"
    validation = render_validation_table(results)
    since = last_tag or "repository start"

    return f"""## v{version} - {date}

Automated patch release cut by `scripts/release/auto_release.py` from
commits merged into `main` since `{since}`. See
`docs/releases/v{version}.md` for full detail.

### Commits included (v{version})

{commit_lines}

### Validation (v{version})

{validation}

### Release Sync (v{version})

- Git tag: `v{version}`
- Repository: <{REPO_URL}>

"""


def prepend_changelog(entry: str) -> None:
    path = ROOT / "CHANGELOG.md"
    text = _read(path)
    marker = "All notable changes to this project are documented in this file.\n"
    idx = text.find(marker)
    if idx == -1:
        raise RuntimeError("CHANGELOG.md marker line not found")
    insert_at = idx + len(marker) + 1  # skip the blank line after marker
    new_text = text[:insert_at] + entry + "\n" + text[insert_at:]
    _write(path, new_text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write files (default: dry-run only prints)")
    parser.add_argument("--print-version-only", action="store_true", help="Print the next version and exit")
    args = parser.parse_args()

    current = get_current_version()
    if args.print_version_only:
        print(bump_patch(current))
        return 0

    last_tag = get_last_tag()
    commits = get_commits_since(last_tag)

    if not commits:
        print("[auto-release] No new commits since last tag; nothing to release.")
        return 3  # distinct code: "no-op", not a failure

    print(f"[auto-release] Current version: {current}")
    print(f"[auto-release] Last tag: {last_tag or '(none)'}")
    print(f"[auto-release] Commits since last tag: {len(commits)}")

    results = run_all_checks()
    for r in results:
        print(f"  - {r.name}: {r.status}")
        if r.status == "FAIL":
            print(f"    {r.detail}")

    failures = [r for r in results if r.status == "FAIL"]
    if failures:
        print(f"[auto-release] {len(failures)} check(s) FAILED. Aborting: no version bump, "
              f"no changelog, no release note, no tag.")
        return 1

    new_version = bump_patch(current)
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if not args.write:
        print(f"[auto-release] DRY RUN: would bump {current} -> {new_version}")
        return 0

    touched = bump_version_files(current, new_version)
    print(f"[auto-release] Bumped version in: {', '.join(touched)}")

    release_note = render_release_note(new_version, date, last_tag, commits, results)
    release_path = ROOT / "docs" / "releases" / f"v{new_version}.md"
    _write(release_path, release_note)
    print(f"[auto-release] Wrote {release_path.relative_to(ROOT)}")

    changelog_entry = render_changelog_entry(new_version, date, last_tag, commits, results)
    prepend_changelog(changelog_entry)
    print("[auto-release] Prepended CHANGELOG.md entry")

    print(f"NEW_VERSION={new_version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
