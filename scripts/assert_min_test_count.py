#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
import sys


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fail CI when collected pytest tests are below a threshold."
    )
    parser.add_argument("--minimum", type=int, default=64)
    parser.add_argument("--pytest-cmd", default="python -m pytest --collect-only -q")
    return parser.parse_args()


def _extract_count(output: str) -> int:
    for line in output.splitlines():
        match = re.search(r"(\d+)\s+tests?\s+collected", line)
        if match:
            return int(match.group(1))
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    if lines and lines[-1].isdigit():
        return int(lines[-1])
    raise ValueError("Could not detect collected test count from pytest output")


def main() -> int:
    args = _parse_args()
    completed = subprocess.run(
        args.pytest_cmd,
        shell=True,
        capture_output=True,
        text=True,
        check=False,
    )

    merged_output = "\n".join(
        part for part in [completed.stdout, completed.stderr] if part
    )
    print(merged_output)

    if completed.returncode != 0:
        print("pytest collection failed", file=sys.stderr)
        return completed.returncode

    collected = _extract_count(merged_output)
    print(f"Collected tests: {collected}")
    print(f"Minimum required: {args.minimum}")

    if collected < args.minimum:
        print(
            f"Test inventory gate failed: {collected} < {args.minimum}",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
