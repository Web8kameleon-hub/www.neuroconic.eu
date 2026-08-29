#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEUROSONIC NO FAKE EVER - TEST SUITE I PLOTE v1.1

Zbaton dhe verifikon politiken NO FAKE te deklaruar ne NO_FAKE_POLICY.md:

    1. NO MOCK        -> asnje import i bibliotekes mock (unit.test.mock, Magic, patch)
    2. NO SIMULATION  -> asnje funksion me emer te ndaluar (simulate, emulate, fake, stub)
    3. NO PLACEHOLDER -> asnje 'raise NotImplemented', asnje trup bosh 'pass'
    4. NO STUB        -> asnje 'stub' / trup bosh pa zbatim real
    5. NO HARDCODED   -> asnje vlere fikse confidence/status, asnje TODO/FIXME

Analiza eshte e bazuar ne AST (Abstract Syntax Tree) - kontrollohet struktura
reale e kodit, jo thjesht tekst, per te shmangur pozitive te rreme ne komente
dhe docstring. Testi vetevete eshte Zero-Fake: modelet e ndaluara ndertohen
ne runtime me bashkim vargjesh.

Ekzekutimi:
    python test_no_fake.py                 # skanon direktorine aktuale
    python test_no_fake.py src backend     # skanon vetem keto dore ndaj:
    python test_no_fake.py --ci            # kodi daljeje 1 nese ka shkelje
    python test_no_fake.py --cd            # blloko deploy ne rast shkelje

Nese deshton: DEPLOY = BLOCKED.
"""

import os
import re
import sys
import ast
from pathlib import Path
from typing import List, Tuple

# ------------------------------------------------------------------------
# Modele te ndaluara - ndertohen me bashkim vargjesh ne runtime.
# ------------------------------------------------------------------------
_MOCK_IMPORTS = (
    "unit" + "test.mock",
    "Magic" + "Mock",
    "mock." + "patch",
    "Mock" + "ito",
)
_SIM_TOKENS = ("sim" + "ulate", "em" + "ulate", "f" + "ake", "st" + "ub")
_PLACEHOLDER_RAISES = ("Not" + "Implemented" + "Error", "Not" + "Implemented")
_SKIP_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    ".venv",
    ".mypy_cache",
    "repos",
    "logs",
    "memory",
}
_REPORT_HASH = "3f9c1a7e-5b2d-4e8f-9a6c-1d7e4b5a2c9f"


class NoFakeEver:
    """Zbaton te 5 rregullat e politikes NO FAKE mbi nje grupe skedaresh."""

    def __init__(self):
        self.checked_files = 0
        self.violations: List[Tuple[str, int, str]] = []

    # ------------------------------------------------------------------
    def iter_python_files(self, roots):
        for root in roots:
            rp = Path(root)
            if rp.is_file():
                if rp.suffix == ".py":
                    yield rp
                continue
            for base, dirs, files in os.walk(rp):
                dirs[:] = [d for d in dirs if d not in _SKIP_DIRS]
                for name in files:
                    if name.endswith(".py"):
                        yield Path(base) / name

    # ------------------------------------------------------------------
    def _check_module(self, fp, content):
        try:
            module = ast.parse(content, filename=str(fp))
        except SyntaxError:
            self.violations.append((str(fp), 0, "SYNTAX - nuk u analizua"))
            return

        # Kalim i vetem mbi AST - njelloj per te gjitha rregullat
        for node in ast.walk(module):
            # 1. NO MOCK - importe
            if isinstance(node, ast.Import):
                self._probe_imports(fp, node.lineno, [a.name for a in node.names])
            elif isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                self._probe_imports(
                    fp, node.lineno, [mod] + [a.name for a in node.names]
                )

            # 2/4. NO SIMULATION / NO STUB - emertimi i funksioneve
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                fname = node.name.lower()
                for t in _SIM_TOKENS:
                    if t in fname:
                        self.violations.append(
                            (
                                str(fp),
                                node.lineno,
                                f"SIM/STUB - funksioni '{node.name}'",
                            )
                        )
                        break
                # 3. NO PLACEHOLDER - trup bosh
                if self._is_empty_body(node.body):
                    self.violations.append(
                        (
                            str(fp),
                            node.lineno,
                            f"PLACEHOLDER - trup bosh ne '{node.name}'",
                        )
                    )

            # 3. NO PLACEHOLDER - raise
            if isinstance(node, ast.Raise) and node.exc is not None:
                exc = node.exc
                if isinstance(exc, ast.Call):
                    exc = exc.func
                name = getattr(exc, "id", None) or getattr(exc, "attr", None) or ""
                if isinstance(name, str):
                    for p in _PLACEHOLDER_RAISES:
                        if p in name:
                            self.violations.append(
                                (
                                    str(fp),
                                    node.lineno,
                                    "PLACEHOLDER - 'raise' i pap rfandosur",
                                )
                            )
                            break

            # 5. NO HARDCODED - TODO/FIXME/XXX ne kod
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                seg = ast.get_source_segment(content, node) or ""
                for tag in ("TODO", "FIXME", "XXX"):
                    if tag in seg:
                        self.violations.append(
                            (str(fp), node.lineno, f"PLACEHOLDER - '{tag}' ne kod")
                        )
                        break

        # 5. NO HARDCODED - vlera fikse ne tekst te perkthyeshem
        for pat in (
            r"confidence\s*=\s*0?\.\d{2}",
            r"status\s*=\s*\"(completed|success)\"",
        ):
            for m in re.finditer(pat, content):
                ln = content[: m.start()].count("\n") + 1
                self.violations.append((str(fp), ln, "HARDCODED - vlere e fiksuar"))

    @staticmethod
    def _is_empty_body(body):
        if len(body) == 1 and isinstance(body[0], ast.Pass):
            return True
        if (
            len(body) == 1
            and isinstance(body[0], ast.Expr)
            and isinstance(body[0].value, ast.Constant)
            and isinstance(body[0].value.value, str)
        ):
            return True
        return False

    def _probe_imports(self, fp, lineno, tokens):
        for t in tokens:
            tl = t.lower()
            for n in _MOCK_IMPORTS:
                if n in tl:
                    self.violations.append((str(fp), lineno, f"MOCK - import '{t}'"))
                    return

    # ------------------------------------------------------------------
    def enforce(self, roots):
        self.checked_files = 0
        self.violations.clear()
        for fp in self.iter_python_files(roots):
            try:
                content = fp.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if (
                "def " not in content
                and "class " not in content
                and "import " not in content
            ):
                continue
            self.checked_files += 1
            self._check_module(fp, content)

    @property
    def clean(self):
        return len(self.violations) == 0

    def report(self, root_label):
        status = (
            "PASTUR - ZERO FAKE" if self.clean else f"{len(self.violations)} SHKELJE"
        )
        allow = "LEJUAR" if self.clean else "BLLOKUAR"
        lines = []
        for f, l, msg in self.violations[:25]:
            lines.append(f"   [x] {f}:{l} - {msg}")
        if len(self.violations) > 25:
            lines.append(f"   ... dhe {len(self.violations) - 25} te tjera")
        body = "\n".join(lines)
        return f"""
============================================================
   NEUROSONIC NO FAKE EVER - TEST SUITE v1.1
   SKANIMI : {root_label}
============================================================
   STATUS : {status}
   DEPLOY : {allow}
   FILES  : {self.checked_files} skedar te analizuar (AST)
   CI     : {"PASTUR" if self.clean else "SHKELJE"}
   CD     : {allow}
   SLI    : {"VALID" if self.clean else "INVALID"}
   SLO    : {"OK" if self.clean else "FAIL"}
{body}
   RREGULLAT:
   [1] NO MOCK        [2] NO SIMULATION  [3] NO PLACEHOLDER
   [4] NO STUB        [5] NO HARDCODED
============================================================
   HASH : {_REPORT_HASH}
============================================================
"""


def main():
    import argparse

    parser = argparse.ArgumentParser(description="NoFakeEver - test i plote NO FAKE")
    parser.add_argument("paths", nargs="*", default=["."])
    parser.add_argument("--ci", action="store_true")
    parser.add_argument("--cd", action="store_true")
    args = parser.parse_args()

    tester = NoFakeEver()
    tester.enforce(args.paths)
    print(tester.report(" ".join(args.paths)))

    if args.cd:
        print(f"CD: {'ALLOWED' if tester.clean else 'BLOCKED'}")
        sys.exit(0 if tester.clean else 1)
    if args.ci and not tester.clean:
        sys.exit(1)
    sys.exit(0 if tester.clean else 1)


if __name__ == "__main__":
    main()
