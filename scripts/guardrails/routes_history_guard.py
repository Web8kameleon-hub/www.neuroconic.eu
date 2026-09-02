#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

MIN_EXPECTED_TOTAL_ROUTES = int(os.environ.get("NEURO_ROUTE_MIN_TOTAL", "2"))
MIN_EXPECTED_PYTHON_ROUTE_FILES = int(os.environ.get("NEURO_ROUTE_MIN_PY", "2"))
MIN_EXPECTED_TS_ROUTE_FILES = int(os.environ.get("NEURO_ROUTE_MIN_TS", "0"))

IGNORED_SEGMENTS = (
    "/node_modules/",
    "/.venv/",
    "/.venv-1/",
    "/__pycache__/",
)


@dataclass
class CheckFailure:
    code: str
    message: str


def _run_git(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git command failed")
    return result.stdout


def _normalize(path: str) -> str:
    return path.strip().replace("\\", "/")


def _should_keep(path: str) -> bool:
    normalized = f"/{path.lstrip('/')}"
    for segment in IGNORED_SEGMENTS:
        if segment in normalized:
            return False
    return True


def _collect_ts_routes() -> list[str]:
    output = _run_git(
        [
            "log",
            "--name-only",
            "--pretty=format:",
            "--",
            "**/route.ts",
            "**/route.tsx",
            "**/route.js",
            "**/route.jsx",
        ]
    )
    rows = [_normalize(line) for line in output.splitlines() if line.strip()]
    return sorted({row for row in rows if _should_keep(row)})


def _collect_python_route_files() -> list[str]:
    regexes = [
        r"app\.get\(",
        r"app\.post\(",
        r"app\.put\(",
        r"app\.delete\(",
        r"app\.patch\(",
        r"router\.get\(",
        r"router\.post\(",
        r"router\.put\(",
        r"router\.delete\(",
        r"router\.patch\(",
    ]

    rows: list[str] = []
    for regex in regexes:
        output = _run_git(["log", "-G", regex, "--name-only", "--pretty=format:", "--", "*.py"])
        rows.extend(_normalize(line) for line in output.splitlines() if line.strip())

    return sorted({row for row in rows if _should_keep(row)})


def main() -> int:
    failures: list[CheckFailure] = []

    try:
        ts_routes = _collect_ts_routes()
        py_routes = _collect_python_route_files()
    except Exception as exc:
        failures.append(CheckFailure("GIT_HISTORY_SCAN_FAILED", str(exc)))
        ts_routes = []
        py_routes = []

    combined = sorted(set(ts_routes) | set(py_routes))

    if len(ts_routes) < MIN_EXPECTED_TS_ROUTE_FILES:
        failures.append(
            CheckFailure(
                "TS_ROUTE_HISTORY_TOO_SMALL",
                f"Expected at least {MIN_EXPECTED_TS_ROUTE_FILES} TS route files, found {len(ts_routes)}",
            )
        )

    if len(py_routes) < MIN_EXPECTED_PYTHON_ROUTE_FILES:
        failures.append(
            CheckFailure(
                "PY_ROUTE_HISTORY_TOO_SMALL",
                f"Expected at least {MIN_EXPECTED_PYTHON_ROUTE_FILES} Python route files, found {len(py_routes)}",
            )
        )

    if len(combined) < MIN_EXPECTED_TOTAL_ROUTES:
        failures.append(
            CheckFailure(
                "ROUTE_HISTORY_TOO_SMALL",
                f"Expected at least {MIN_EXPECTED_TOTAL_ROUTES} total route files, found {len(combined)}",
            )
        )

    report = {
        "ok": len(failures) == 0,
        "minimums": {
            "ts": MIN_EXPECTED_TS_ROUTE_FILES,
            "python": MIN_EXPECTED_PYTHON_ROUTE_FILES,
            "combined": MIN_EXPECTED_TOTAL_ROUTES,
        },
        "counts": {
            "ts": len(ts_routes),
            "python": len(py_routes),
            "combined": len(combined),
        },
        "failures": [failure.__dict__ for failure in failures],
        "samples": {
            "ts_first_20": ts_routes[:20],
            "python_first_20": py_routes[:20],
            "combined_first_20": combined[:20],
        },
    }

    out = ROOT / "docs" / "production" / "canonical" / "routes_history_guard_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=True), encoding="utf-8")

    if failures:
        print("[ROUTES-HISTORY-GUARD] FAIL")
        for failure in failures:
            print(f"- {failure.code}: {failure.message}")
        print(f"Report: {out.relative_to(ROOT)}")
        return 1

    print("[ROUTES-HISTORY-GUARD] PASS")
    print(f"Counts => ts={len(ts_routes)}, python={len(py_routes)}, combined={len(combined)}")
    print(f"Report: {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())