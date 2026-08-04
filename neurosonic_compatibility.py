#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEUROSONIC COMPATIBILITY MATRIX - VERIFIKON PARA INSTALIMIT
Nëse dështon: INSTALL = BLOCKED

Niveli 2.5 i Arkitekturës Neurosonic Trinity+ASI
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
import json
from neurosonic_dna import NeurosonicDNA
from neurosonic_genome import NeurosonicGenome


@dataclass
class CompatibilityResult:
    """Rezultati i verifikimit të përputhshmërisë"""

    module_id: str
    module_name: str
    compatible: bool
    checks: Dict[str, bool] = field(default_factory=dict)
    violations: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)


class NeurosonicCompatibilityMatrix:
    """
    Matrica e përputhshmërisë - verifikon modulet para instalimit.

    Nëse ndonjë kontroll dështon, INSTALL = BLOCKED.
    Kjo nuk do të thotë se moduli është i keq,
    por se nuk përputhet me ADN-në e ekosistemit.
    """

    def __init__(self, dna: NeurosonicDNA, genome: NeurosonicGenome):
        self.dna = dna
        self.genome = genome
        self.checks = [
            "constitution_compatibility",
            "genome_compatibility",
            "api_compatibility",
            "memory_compatibility",
            "security_compatibility",
            "performance_compatibility",
            "license_compatibility",
            "data_compatibility",
        ]

    def verify_module(self, module_id: str, module_config: Dict) -> CompatibilityResult:
        """
        Verifikon nëse një modul është i përputhshëm me ekosistemin.

        Args:
            module_id: ID e modulit
            module_config: Konfigurimi i modulit

        Returns:
            CompatibilityResult me rezultatin e verifikimit
        """
        violations = []
        checks = {}

        # 1. Kontrollo DNA-në (Kushtetutë + Siguri + Data + API)
        dna_result = self.dna.verify_module(module_id, module_config)
        checks["constitution_compatibility"] = dna_result["compatible"]
        if not dna_result["compatible"]:
            violations.extend(dna_result["violations"])

        # 2. Kontrollo Genome-në (varësitë)
        genome_result = self._verify_genome_compatibility(module_config)
        checks["genome_compatibility"] = genome_result["compatible"]
        if not genome_result["compatible"]:
            violations.extend(genome_result["violations"])

        # 3. Kontrollo API-të
        api_result = self._verify_api_compatibility(module_config)
        checks["api_compatibility"] = api_result["compatible"]
        if not api_result["compatible"]:
            violations.extend(api_result["violations"])

        # 4. Kontrollo Memories
        memory_result = self._verify_memory_compatibility(module_config)
        checks["memory_compatibility"] = memory_result["compatible"]
        if not memory_result["compatible"]:
            violations.extend(memory_result["violations"])

        # 5. Kontrollo Sigurinë
        security_result = self._verify_security_compatibility(module_config)
        checks["security_compatibility"] = security_result["compatible"]
        if not security_result["compatible"]:
            violations.extend(security_result["violations"])

        # 6. Kontrollo Performancën
        perf_result = self._verify_performance_compatibility(module_config)
        checks["performance_compatibility"] = perf_result["compatible"]
        if not perf_result["compatible"]:
            violations.extend(perf_result["violations"])

        # 7. Kontrollo Licencën
        license_result = self._verify_license_compatibility(module_config)
        checks["license_compatibility"] = license_result["compatible"]
        if not license_result["compatible"]:
            violations.extend(license_result["violations"])

        # 8. Kontrollo të Dhënat
        data_result = self._verify_data_compatibility(module_config)
        checks["data_compatibility"] = data_result["compatible"]
        if not data_result["compatible"]:
            violations.extend(data_result["violations"])

        # Nëse ndonjë kontroll dështon, INSTALL = BLOCKED
        compatible = all(checks.values())

        return CompatibilityResult(
            module_id=module_id,
            module_name=module_config.get("name", module_id),
            compatible=compatible,
            checks=checks,
            violations=violations,
            details={
                "dna": dna_result,
                "genome": genome_result,
                "api": api_result,
                "memory": memory_result,
                "security": security_result,
                "performance": perf_result,
                "license": license_result,
                "data": data_result,
            },
        )

    def _verify_genome_compatibility(self, config: Dict) -> Dict[str, Any]:
        """Verifikon nëse moduli përputhet me Genome-në"""
        violations = []
        dependencies = config.get("dependencies", [])

        for dep in dependencies:
            if dep not in self.genome.packages:
                violations.append(f"Dependency {dep} not found in Genome")

        return {
            "compatible": len(violations) == 0,
            "violations": violations,
        }

    def _verify_api_compatibility(self, config: Dict) -> Dict[str, Any]:
        """Verifikon nëse API-të përputhen"""
        violations = []

        # Kontrollo nëse moduli ka API të versionuar
        if "api_version" not in config:
            violations.append("Missing api_version - API versioning required")

        # Kontrollo nëse moduli ka path API
        if "api_path" not in config:
            violations.append("Missing api_path - API path required")

        return {
            "compatible": len(violations) == 0,
            "violations": violations,
        }

    def _verify_memory_compatibility(self, config: Dict) -> Dict[str, Any]:
        """Verifikon nëse memoria përputhet"""
        violations = []

        # Kontrollo nëse moduli respekton HVO
        memory_type = config.get("memory_type", "")
        if not memory_type:
            violations.append("Missing memory_type - HVO compliance required")
        elif memory_type.upper() not in ["HVO", "HORIZONTAL", "VERTICAL", "ORBITAL"]:
            violations.append(f"Memory type '{memory_type}' not compatible - use HVO")

        return {
            "compatible": len(violations) == 0,
            "violations": violations,
        }

    def _verify_security_compatibility(self, config: Dict) -> Dict[str, Any]:
        """Verifikon nëse siguria përputhet"""
        violations = []

        # Kontrollo nëse moduli ka kriptim
        encryption = config.get("encryption", "")
        if not encryption:
            violations.append("Missing encryption - encryption required")

        # Kontrollo nëse moduli ka Zero Trust
        zero_trust = config.get("zero_trust", False)
        if not zero_trust:
            violations.append("zero_trust must be True")

        return {
            "compatible": len(violations) == 0,
            "violations": violations,
        }

    def _verify_performance_compatibility(self, config: Dict) -> Dict[str, Any]:
        """Verifikon nëse performanca përputhet"""
        violations = []

        # Kontrollo nëse moduli ka SSE
        sse_support = config.get("sse_support", False)
        tide_compatible = config.get("tide_compatible", False)

        if not sse_support:
            violations.append("Missing SSE support - streaming required")

        if not tide_compatible:
            violations.append("Not Tide compatible - adaptive flow required")

        return {
            "compatible": len(violations) == 0,
            "violations": violations,
        }

    def _verify_license_compatibility(self, config: Dict) -> Dict[str, Any]:
        """Verifikon nëse licenca përputhet"""
        violations = []
        allowed_licenses = [
            "MIT",
            "Apache",
            "GPL",
            "Neurosonic",
            "Neurosonic-Enterprise",
        ]

        license_type = config.get("license", "")
        if not license_type:
            violations.append("Missing license type")
        elif license_type not in allowed_licenses:
            violations.append(
                f"License '{license_type}' not allowed. Allowed: {', '.join(allowed_licenses)}"
            )

        return {
            "compatible": len(violations) == 0,
            "violations": violations,
        }

    def _verify_data_compatibility(self, config: Dict) -> Dict[str, Any]:
        """Verifikon nëse të dhënat përputhen me CUDM"""
        violations = []

        # Kontrollo nëse moduli përdor CUDM
        if not config.get("cudm_compatible", False):
            violations.append(
                "Module not CUDM compatible - Unified Data Model required"
            )

        # Kontrollo nëse moduli respekton user data ownership
        if not config.get("user_data_ownership", True):
            violations.append("user_data_ownership must be True - user owns their data")

        return {
            "compatible": len(violations) == 0,
            "violations": violations,
        }

    def generate_report(self, result: CompatibilityResult) -> str:
        """Gjeneron një raport të lexueshëm të verifikimit"""
        report = []
        report.append("=" * 70)
        report.append(
            f"📋 COMPATIBILITY REPORT: {result.module_name} ({result.module_id})"
        )
        report.append("=" * 70)
        report.append(
            f"📊 Status: {'✅ COMPATIBLE' if result.compatible else '❌ BLOCKED'}"
        )

        report.append(f"\n📋 Checks:")
        for check, passed in result.checks.items():
            status = "✅" if passed else "❌"
            report.append(f"   {status} {check}")

        if result.violations:
            report.append(f"\n⚠️ Violations:")
            for violation in result.violations:
                report.append(f"   ❌ {violation}")

        if result.compatible:
            report.append(
                f"\n✅ INSTALL ALLOWED - Module compatible with Neurosonic DNA"
            )
        else:
            report.append(
                f"\n🚫 INSTALL = BLOCKED - Module not compatible with Neurosonic DNA"
            )
            report.append(f"   Nuk do të thotë se moduli është i keq.")
            report.append(f"   Por se nuk përputhet me ADN-në e ekosistemit.")

        report.append("=" * 70)
        return "\n".join(report)


# Test i shpejtë
if __name__ == "__main__":
    from neurosonic_dna import NeurosonicDNA
    from neurosonic_genome import NeurosonicGenome

    dna = NeurosonicDNA()
    genome = NeurosonicGenome()
    matrix = NeurosonicCompatibilityMatrix(dna, genome)

    # Test 1: Modul i përputhshëm
    print("\n🔍 TEST 1: MODUL I PËRPUTHSHËM")
    good_module = {
        "name": "CLX Vision Pro",
        "api_version": "2.0",
        "api_path": "/api/v2/vision",
        "memory_type": "HVO",
        "encryption": "AES256",
        "zero_trust": True,
        "sse_support": True,
        "tide_compatible": True,
        "license": "Neurosonic",
        "cudm_compatible": True,
        "user_data_ownership": True,
        "dependencies": ["NGI-CORE-0001", "NGI-AI-0004"],
        "constitution_compatibility": [
            "G001",
            "G002",
            "G003",
            "G004",
            "G005",
            "G006",
            "G007",
            "G008",
            "G009",
            "G010",
        ],
        "security_compatibility": [
            "SR001",
            "SR002",
            "SR003",
            "SR004",
            "SR005",
            "SR006",
            "SR007",
            "SR008",
        ],
        "data_compatibility": ["DR001", "DR002", "DR003", "DR004", "DR005"],
        "api_compatibility": ["AR001", "AR002", "AR003", "AR004"],
    }

    result1 = matrix.verify_module("MOD-001", good_module)
    print(matrix.generate_report(result1))

    # Test 2: Modul i papërputhshëm
    print("\n🔍 TEST 2: MODUL I PAPËRPUTHSHËM")
    bad_module = {
        "name": "External AI Service",
        "license": "Proprietary",
        "zero_trust": False,
        "user_data_ownership": False,
        "dependencies": ["NGI-CORE-0001", "NGI-CORE-9999"],
    }

    result2 = matrix.verify_module("MOD-002", bad_module)
    print(matrix.generate_report(result2))
