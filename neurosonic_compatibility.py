#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEUROSONIC COMPATIBILITY MATRIX - INSTALL = BLOCKED
Verifikon përputhshmërinë e çdo moduli me DNA-në dhe Genome-në.

8 kontrolle:
1. Constitution Compatibility
2. Genome Compatibility
3. API Compatibility
4. Memory Compatibility
5. Security Compatibility
6. Performance Compatibility
7. License Compatibility
8. Data Compatibility
"""

import hashlib
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class CompatibilityResult:
    """Rezultat i verifikimit të përputhshmërisë"""

    module_id: str
    compatible: bool
    violations: List[str]
    checks: Dict[str, bool]
    score: float
    timestamp: float
    hash: str


class NeurosonicCompatibilityMatrix:
    """
    Compatibility Matrix - verifikon përputhshmërinë e moduleve.

    Nëse dështon: INSTALL = BLOCKED
    """

    def __init__(self, dna, genome):
        self.dna = dna
        self.genome = genome
        self.checks = {}
        print("🔍 Compatibility Matrix inicializuar")

    def verify_module(self, module_id: str, module_config: Dict) -> CompatibilityResult:
        """Verifikon nëse një modul është i përputhshëm"""
        violations = []
        checks = {}

        # 1. Constitution Compatibility
        dna_check = self.dna.verify_module(module_id, module_config)
        checks["constitution_compatibility"] = dna_check["compatible"]
        if not dna_check["compatible"]:
            violations.extend(dna_check["violations"])

        # 2. Genome Compatibility
        genome_ok = self._check_genome(module_config.get("dependencies", []))
        checks["genome_compatibility"] = genome_ok
        if not genome_ok:
            violations.append("Missing genome dependencies")

        # 3. API Compatibility
        api_ok = self._check_api(module_config)
        checks["api_compatibility"] = api_ok
        if not api_ok:
            violations.append("API compatibility check failed")

        # 4. Memory Compatibility
        memory_ok = self._check_memory(module_config)
        checks["memory_compatibility"] = memory_ok
        if not memory_ok:
            violations.append("Memory compatibility check failed")

        # 5. Security Compatibility
        security_ok = self._check_security(module_config)
        checks["security_compatibility"] = security_ok
        if not security_ok:
            violations.append("Security check failed")

        # 6. Performance Compatibility
        perf_ok = self._check_performance(module_config)
        checks["performance_compatibility"] = perf_ok
        if not perf_ok:
            violations.append("Performance check failed")

        # 7. License Compatibility
        license_ok = self._check_license(module_config)
        checks["license_compatibility"] = license_ok
        if not license_ok:
            violations.append("License check failed")

        # 8. Data Compatibility
        data_ok = self._check_data(module_config)
        checks["data_compatibility"] = data_ok
        if not data_ok:
            violations.append("Data compatibility check failed")

        self.checks[module_id] = checks

        # Llogarit score
        passed = sum(1 for v in checks.values() if v)
        score = (passed / len(checks)) * 100 if checks else 0

        return CompatibilityResult(
            module_id=module_id,
            compatible=len(violations) == 0,
            violations=violations,
            checks=checks,
            score=score,
            timestamp=time.time(),
            hash=hashlib.sha256(f"{module_id}{time.time()}".encode()).hexdigest()[:12],
        )

    def _check_genome(self, dependencies: List[str]) -> bool:
        """Kontrollon nëse varësitë ekzistojnë në Genome"""
        for dep in dependencies:
            if not self.genome.get_package(dep):
                return False
        return True

    def _check_api(self, config: Dict) -> bool:
        """Kontrollon përputhshmërinë API"""
        if config.get("cudm_compatible") == False:
            return False
        if config.get("api_path") and not config.get("api_version"):
            return False
        return True

    def _check_memory(self, config: Dict) -> bool:
        """Kontrollon përputhshmërinë e memories"""
        if config.get("memory_type") and config["memory_type"] != "HVO":
            return False
        return True

    def _check_security(self, config: Dict) -> bool:
        """Kontrollon kushtet e sigurisë"""
        if config.get("encryption") is None:
            return False
        if config.get("zero_trust") == False:
            return False
        return True

    def _check_performance(self, config: Dict) -> bool:
        """Kontrollon kushtet e performancës"""
        if config.get("sse_support") == False:
            return False
        if config.get("tide_compatible") == False:
            return False
        return True

    def _check_license(self, config: Dict) -> bool:
        """Kontrollon licencën"""
        if config.get("license") == "Proprietary":
            return False
        return True

    def _check_data(self, config: Dict) -> bool:
        """Kontrollon rregullat e të dhënave"""
        if config.get("user_data_ownership") == False:
            return False
        if config.get("cudm_compatible") == False:
            return False
        return True

    def generate_report(self, result: CompatibilityResult) -> str:
        """Gjeneron raport të detajuar"""
        status = "✅ INSTALL ALLOWED" if result.compatible else "❌ INSTALL = BLOCKED"
        report = f"""
{"=" * 60}
🔍 COMPATIBILITY MATRIX REPORT
{"=" * 60}
Module: {result.module_id}
Status: {status}
Score: {result.score:.0f}%
{"=" * 60}
Checks:
"""
        for check, passed in result.checks.items():
            icon = "✅" if passed else "❌"
            report += f"  {icon} {check}\n"

        if result.violations:
            report += f"\n⚠️ Violations:\n"
            for v in result.violations:
                report += f"  - {v}\n"

        report += f"\nHash: {result.hash}"
        return report
