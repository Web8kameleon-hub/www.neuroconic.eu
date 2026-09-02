#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEUROSONIC NO FAKE POLICE - ZERO FAKE, ZERO MOCK, ZERO SIMULATION
CI/CD/SLI/SLO/CLI/CLO - Kontrollon VETEM kod real (jo komente)
"""

import os
import sys
import re
import datetime
from pathlib import Path
from typing import List, Tuple, Dict, Optional, Any


class NoFakePolice:
    """NO FAKE POLICE - kontrollon kodin per fake/mock/simulation/placeholder"""

    def __init__(self, paths: Optional[List[str]] = None):
        self.paths = [Path(p) for p in (paths or ["."])]
        self.violations: List[Tuple[str, int, str, str]] = []
        self.checked_files = 0
        self.clean_files = 0

    def is_real_code(self, lines: List[str], line_num: int) -> bool:
        """Kthen True nese rreshti eshte kod real (jo koment/docstring)"""
        if line_num < 1 or line_num > len(lines):
            return False
        in_multiline = False
        for i, line in enumerate(lines, 1):
            s = line.strip()
            if s.startswith('"""') or s.startswith("'''"):
                in_multiline = not in_multiline
            if i == line_num:
                if in_multiline or s.startswith("#"):
                    return False
                return True
        return True

    def enforce(self):
        self.violations.clear()
        self.checked_files = 0
        self.clean_files = 0

        forbidden_mocks = [
            "unittest.mock",
            "MagicMock",
            "mock.patch",
            "@mock.patch",
            "Mock()",
        ]
        # Patterns encoded to avoid self-detection
        forbidden_sim = [r"def " + "simulate", r"def _" + "simulate", r"def _" + "fake_", r"def _" + "stub"]
        forbidden_placeholder = [r"NotImplemented" + "Error", r"NotImplemented"]

        for base_path in self.paths:
            if not base_path.exists():
                continue
            for root, dirs, files in os.walk(base_path):
                dirs[:] = [
                    d
                    for d in dirs
                    if d
                    not in [
                        ".git",
                        "__pycache__",
                        "node_modules",
                        ".venv",
                        ".venv-1",
                        ".mypy_cache",
                        "neurosonic.egg-info",
                        ".pytest_cache",
                        "build",
                        "dist",
                        ".eggs",
                    ]
                ]
                for file in files:
                    if not file.endswith(".py"):
                        continue
                    fp = os.path.join(root, file)
                    self.checked_files += 1
                    try:
                        with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                            lines = content.split("\n")
                    except Exception:
                        continue

                    has_violation = False

                    # Kontrollo importe te ndaluara - VETEM ne kod real
                    for i, line in enumerate(lines, 1):
                        s = line.strip()
                        if s.startswith(("from ", "import ")) and self.is_real_code(
                            lines, i
                        ):
                            for m in forbidden_mocks:
                                if m in s:
                                    self.violations.append(
                                        (fp, i, "CI-MOCK", f"import '{s[:60]}'")
                                    )
                                    has_violation = True

                    # Kontrollo funksione simulimi - VETEM ne kod real
                    for pat in forbidden_sim:
                        for match in re.finditer(pat, content):
                            ln = content[: match.start()].count("\n") + 1
                            if self.is_real_code(lines, ln):
                                self.violations.append(
                                    (fp, ln, "CI-SIM", f"simulation '{match.group()}'")
                                )
                                has_violation = True

                    # Kontrollo placeholder - VETEM ne kod real
                    for pat in forbidden_placeholder:
                        for match in re.finditer(pat, content):
                            ln = content[: match.start()].count("\n") + 1
                            if self.is_real_code(lines, ln):
                                if os.path.basename(fp) in (
                                    "neurosonic_no_fake_police.py",
                                    "test_no_fake.py",
                                ):
                                    continue
                                s = lines[ln - 1].strip()
                                self.violations.append(
                                    (
                                        fp,
                                        ln,
                                        "CI-PL",
                                        f"placeholder '{match.group()}' in '{s[:60]}'",
                                    )
                                )
                                has_violation = True

                    if not has_violation:
                        self.clean_files += 1

    def report(self) -> str:
        self.enforce()
        status = "PASTUR" if not self.violations else f"{len(self.violations)} SHKELJE"
        deploy = "LEJUAR" if not self.violations else "BLLOKUAR"
        lines = []
        for f, l, r, d in self.violations[:10]:
            lines.append(f"   [{r}] {f}:{l} - {d}")
        ci = "PASTUR" if not self.violations else "SHKELJE"
        return (
            f"\n{'=' * 60}\n   NO FAKE POLICE\n{'=' * 60}\n"
            f"   STATUS: {status}   DEPLOY: {deploy}\n"
            f"   Files: {self.checked_files}  Clean: {self.clean_files}\n"
            f"   CI: {ci}  CD: {deploy}\n"
            f"   SLI: {'VALID' if not self.violations else 'INVALID'}\n"
            f"   SLO: {'OK' if not self.violations else 'FAIL'}\n"
            f"   CLO: {'STABLE' if not self.violations else 'RISK'}\n"
            + ("\n".join(lines) + "\n" if lines else "")
            + f"{'=' * 60}\n"
        )


def main():
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("paths", nargs="*", default=["."])
    p.add_argument("--ci", action="store_true")
    p.add_argument("--cd", action="store_true")
    args = p.parse_args()
    police = NoFakePolice(paths=args.paths)
    if args.cd:
        police.enforce()
        ok = len(police.violations) == 0
        print(f"CD: {'ALLOWED' if ok else 'BLOCKED'}")
        sys.exit(0 if ok else 1)
    print(police.report())
    if args.ci and police.violations:
        sys.exit(1)


if __name__ == "__main__":
    main()
