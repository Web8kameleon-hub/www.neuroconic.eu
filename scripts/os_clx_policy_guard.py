#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None


@dataclass
class PolicyFinding:
    severity: str
    rule_id: str
    message: str
    hint: str


def _load_policy(policy_path: Path) -> dict[str, Any]:
    raw = policy_path.read_text(encoding="utf-8")
    return json.loads(raw)


def _read_pyproject(repo_root: Path) -> dict[str, Any]:
    if tomllib is None:
        return {}
    pyproject_path = repo_root / "pyproject.toml"
    if not pyproject_path.exists():
        return {}
    return tomllib.loads(pyproject_path.read_text(encoding="utf-8"))


def _safe_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _iter_repo_files(repo_root: Path) -> list[Path]:
    excluded = {
        ".git",
        "__pycache__",
        ".venv",
        ".venv-1",
        ".mypy_cache",
        ".pytest_cache",
        "node_modules",
        "dist",
        "build",
        "target",
    }
    files: list[Path] = []
    for root, dirs, filenames in os.walk(repo_root):
        dirs[:] = [d for d in dirs if d not in excluded]
        for filename in filenames:
            files.append(Path(root) / filename)
    return files


def evaluate(repo_root: Path, policy: dict[str, Any]) -> list[PolicyFinding]:
    findings: list[PolicyFinding] = []
    rules = policy.get("rules", {})
    repo_files = _iter_repo_files(repo_root)

    max_repo_files = _safe_int(rules.get("max_repo_files"), 20000)
    if len(repo_files) > max_repo_files:
        findings.append(
            PolicyFinding(
                severity="warning",
                rule_id="OSCLX-WEIGHT-001",
                message=f"Repo file count is {len(repo_files)} (> {max_repo_files}).",
                hint="Archive old generated artifacts and keep core repo slim.",
            )
        )

    max_file_mb = float(rules.get("max_tracked_file_mb", 5))
    max_file_bytes = int(max_file_mb * 1024 * 1024)
    allowed_big_suffixes = tuple(rules.get("allowed_large_file_suffixes", []))
    for file_path in repo_files:
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() in allowed_big_suffixes:
            continue
        try:
            size = file_path.stat().st_size
        except OSError:
            continue
        if size > max_file_bytes:
            findings.append(
                PolicyFinding(
                    severity="warning",
                    rule_id="OSCLX-WEIGHT-002",
                    message=(
                        f"Large file detected: {file_path.relative_to(repo_root)} "
                        f"({size / (1024 * 1024):.2f} MB)."
                    ),
                    hint=f"Move large artifacts outside git or raise threshold in policy manifest.",
                )
            )

    required_paths = rules.get("required_paths", [])
    for relative in required_paths:
        if not (repo_root / relative).exists():
            findings.append(
                PolicyFinding(
                    severity="error",
                    rule_id="OSCLX-CORE-001",
                    message=f"Required path missing: {relative}",
                    hint="Restore/create required governance and SEO/runtime files.",
                )
            )

    pyproject = _read_pyproject(repo_root)
    project_scripts = pyproject.get("project", {}).get("scripts", {}) if pyproject else {}
    required_scripts = rules.get("required_python_scripts", [])
    for script_name in required_scripts:
        if script_name not in project_scripts:
            findings.append(
                PolicyFinding(
                    severity="error",
                    rule_id="OSCLX-PYPI-001",
                    message=f"PyPI script entry missing: {script_name}",
                    hint="Add it under [project.scripts] in pyproject.toml.",
                )
            )

    npm_package = repo_root / "packages" / "npm" / "neurosonic-shell" / "package.json"
    crate_manifest = repo_root / "packages" / "crates" / "neurosonic-shell" / "Cargo.toml"
    if rules.get("require_multi_ecosystem_metadata", True):
        if not npm_package.exists():
            findings.append(
                PolicyFinding(
                    severity="warning",
                    rule_id="OSCLX-NPM-001",
                    message="npm package manifest missing for neurosonic-shell.",
                    hint="Keep npm package present for JS ecosystem reach.",
                )
            )
        if not crate_manifest.exists():
            findings.append(
                PolicyFinding(
                    severity="warning",
                    rule_id="OSCLX-CRATE-001",
                    message="Cargo manifest missing for neurosonic-shell crate.",
                    hint="Keep crates package present for Rust ecosystem reach.",
                )
            )

    if rules.get("cloudflare_readiness", True):
        cloudflare_paths = [
            "robots.txt",
            "sitemap.xml",
            "manifest.webmanifest",
        ]
        for relative in cloudflare_paths:
            if not (repo_root / relative).exists():
                findings.append(
                    PolicyFinding(
                        severity="warning",
                        rule_id="OSCLX-CF-001",
                        message=f"Cloudflare/web readiness file missing: {relative}",
                        hint="Add missing web metadata file for CDN/indexing compatibility.",
                    )
                )

    return findings


def _print_report(findings: list[PolicyFinding], strict: bool) -> int:
    errors = [f for f in findings if f.severity == "error"]
    warnings = [f for f in findings if f.severity == "warning"]

    print("=" * 66)
    print("OS-CLX POLICY GUARD (Lightweight)")
    print("=" * 66)
    print(f"Errors: {len(errors)} | Warnings: {len(warnings)} | Strict: {strict}")

    if findings:
        for finding in findings:
            print(
                f"[{finding.severity.upper()}] {finding.rule_id} - "
                f"{finding.message} | Hint: {finding.hint}"
            )
    else:
        print("All OS-CLX policy checks passed.")

    print("=" * 66)
    if strict:
        return 1 if findings else 0
    return 1 if errors else 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="OS-CLX policy guard for lightweight, multi-ecosystem repository hygiene."
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root path. Default: current directory.",
    )
    parser.add_argument(
        "--policy",
        default="docs/governance/OS_CLX_POLICY_PROFILE.json",
        help="Path to OS-CLX policy manifest JSON.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on warnings as well (CI hard mode).",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    policy_path = (repo_root / args.policy).resolve()
    if not policy_path.exists():
        print(f"Policy file not found: {policy_path}")
        sys.exit(2)

    policy = _load_policy(policy_path)
    findings = evaluate(repo_root=repo_root, policy=policy)
    exit_code = _print_report(findings=findings, strict=args.strict)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()