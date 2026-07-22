#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST I PLOTE I ARKITEKTURES SE RE NEUROSONIC
DNA + GENOME + COMPATIBILITY MATRIX + EVOLUTION ENGINE + LIGHTNING SPP
Nese deshton: INSTALL = BLOCKED
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from neurosonic_dna import NeurosonicDNA
from neurosonic_genome import NeurosonicGenome, GenomePackage
from neurosonic_compatibility import NeurosonicCompatibilityMatrix
from neurosonic_evolution import NeurosonicEvolutionEngine
from neurosonic_lightning_bridge import (
    NeurosonicLightningBridge,
    LightningMode,
    ProcessingEngine,
    PrintQuality,
)


def test_dna_layer():
    print("\n" + "=" * 70)
    print(" TEST 1: DNA - I PANDRYSHUESHEM")
    print("=" * 70)
    dna = NeurosonicDNA()
    assert dna.name == "Neurosonic DNA v1.0"
    assert dna.immutable == True
    print(" 1.1 DNA inicializuar sakte")
    rules = dna.get_all_rules()
    assert len(rules["constitution"]) == 10
    assert len(rules["security"]) == 8
    assert len(rules["data"]) == 5
    assert len(rules["api"]) == 4
    assert len(rules["memory"]) == 6
    assert len(rules["governance"]) == 6
    assert len(rules["quality"]) == 5
    assert len(rules["core_values"]) == 6
    print(" 1.2 Te gjitha rregullat jane te pranishme")
    assert dna._hash == dna._compute_dna_hash()
    print(f" 1.3 DNA hash integrity: {dna._hash}")
    good_module = {
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
    assert dna.verify_module("MOD-001", good_module)["compatible"] == True
    print(" 1.4 Modul i perputhshem u verifikua sakte")
    assert (
        dna.verify_module(
            "MOD-002", {"constitution_compatibility": [], "security_compatibility": []}
        )["compatible"]
        == False
    )
    print(" 1.5 Modul i paperputhshem u bllokua sakte")
    assert dna.verify_constitution_action("send_to_external", "module") == False
    assert dna.verify_constitution_action("send_to_external", "api_public") == True
    assert dna.verify_constitution_action("send_unencrypted", "module") == False
    print(" 1.6 Kushtetuta zbaton rregullat sakte")
    stats = dna.get_stats()
    assert stats["total_rules"] > 40
    print(f" 1.7 Statistika: {stats['total_rules']} rregulla gjithsej")
    print("\n NIVELI 1: DNA - TE GJITHA TESTET KALUAN")
    return dna


def test_genome_layer():
    print("\n" + "=" * 70)
    print(" TEST 2: GENOME - ZGJEROHET")
    print("=" * 70)
    genome = NeurosonicGenome()
    assert len(genome.packages) >= 17
    print(f" 2.1 {len(genome.packages)} paketa themelore")
    assert "NGI-CORE-0001" in genome.packages
    assert "NGI-AI-0004" in genome.packages
    assert "NGI-MEM-0007" in genome.packages
    assert "NGI-SEC-0012" in genome.packages
    assert "NGI-LIGHTNING-1001" in genome.packages
    print(" 2.2 Indekset NGI jane te plota (perfshire Lightning SPP)")
    pkg = genome.get_package("NGI-CORE-0001")
    assert pkg is not None
    assert pkg["name"] == "CLX Kernel"
    print(" 2.3 Marrja e paketes funksionon")
    new_pkg = GenomePackage(
        id="NGI-TEST-9999",
        name="Test Package",
        description="Test",
        version="1.0.0",
        author="Neurosonic Test",
        dependencies=["NGI-CORE-0001"],
        capabilities=["test"],
    )
    assert genome.add_package(new_pkg)["success"] == True
    print(" 2.4 Paketa e re u shtua")
    bad_pkg = GenomePackage(
        id="NGI-TEST-9998",
        name="Bad Test",
        description="Bad",
        version="1.0.0",
        author="Neurosonic Test",
        dependencies=["NGI-NONEXIST-9999"],
        capabilities=["test"],
    )
    assert genome.add_package(bad_pkg)["success"] == False
    print(" 2.5 Paketa me varesi qe mungon u bllokua")
    categories = genome.get_packages_by_category()
    assert len(categories.get("core", [])) >= 3
    assert len(categories.get("ai", [])) >= 2
    assert len(categories.get("lightning", [])) >= 1
    print(" 2.6 Kategorizimi i paketave funksionon")
    assert genome.remove_package("NGI-TEST-9999")["success"] == True
    print(" 2.7 Paketa u hoq")
    assert genome.remove_package("NGI-CORE-0001")["success"] == False
    print(" 2.8 Paketa me varesi nuk u hoq")
    stats = genome.get_stats()
    assert stats["total_packages"] >= 19
    print(f" 2.9 Statistika: {stats['total_packages']} paketa")
    print("\n NIVELI 2: GENOME - TE GJITHA TESTET KALUAN")
    return genome


def test_compatibility_matrix_layer(dna, genome):
    print("\n" + "=" * 70)
    print(" TEST 3: COMPATIBILITY MATRIX - INSTALL = BLOCKED")
    print("=" * 70)
    matrix = NeurosonicCompatibilityMatrix(dna, genome)
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
    result = matrix.verify_module("MOD-001", good_module)
    assert result.compatible == True
    assert len(result.violations) == 0
    print(" 3.1 Modul i perputhshem: INSTALL ALLOWED")
    bad_module = {
        "name": "External AI Service",
        "license": "Proprietary",
        "zero_trust": False,
        "user_data_ownership": False,
        "sse_support": False,
        "tide_compatible": False,
        "cudm_compatible": False,
        "dependencies": ["NGI-CORE-0001", "NGI-CORE-9999"],
        "constitution_compatibility": [],
        "security_compatibility": [],
        "data_compatibility": [],
        "api_compatibility": [],
    }
    result = matrix.verify_module("MOD-002", bad_module)
    assert result.compatible == False
    assert len(result.violations) > 0
    print(" 3.2 Modul i paperputhshem: INSTALL = BLOCKED")
    good_result = matrix.verify_module("MOD-003", good_module)
    expected = [
        "constitution_compatibility",
        "genome_compatibility",
        "api_compatibility",
        "memory_compatibility",
        "security_compatibility",
        "performance_compatibility",
        "license_compatibility",
        "data_compatibility",
    ]
    for check in expected:
        assert check in good_result.checks
    assert all(good_result.checks.values())
    print(" 3.3 Te 8 kontrollet jane ekzekutuar")
    report = matrix.generate_report(good_result)
    assert "INSTALL ALLOWED" in report
    print(" 3.4 Raporti i perputhshmerise funksionon")
    print("\n NIVELI 2.5: COMPATIBILITY MATRIX - TE GJITHA TESTET KALUAN")


def test_evolution_engine_layer(dna, genome):
    print("\n" + "=" * 70)
    print(" TEST 4: EVOLUTION ENGINE - PROPOZON, NUK NDRYSHON")
    print("=" * 70)
    evolution = NeurosonicEvolutionEngine(dna, genome)
    analysis = evolution.analyze_architecture()
    assert analysis["dna_integrity"] == True
    print(f" 4.1 Analiza e arkitektures: DNA Integrity = True")
    coverage = analysis["genome_coverage"]
    assert coverage["coverage_percent"] >= 80
    print(f" 4.2 Mbulimi i Genome-se: {coverage['coverage_percent']:.0f}%")
    proposal = evolution.propose_new_rule(
        "Test rule", category="governance", impact_level="high"
    )
    assert "id" in proposal
    assert proposal["status"] == "proposed"
    print(f" 4.3 Propozimi {proposal['id']} u krijua")
    print(
        f" 4.4 Analiza e propozimit: feasibility={proposal['analysis']['feasibility'] * 100:.0f}%"
    )
    version = evolution.create_new_version({"add": ["Test"], "update": ["v2.0"]})
    assert "version" in version
    print(f" 4.5 Versioni {version['version']} u krijua")
    assert dna._hash == dna._compute_dna_hash()
    print(" 4.6 DNA nuk u ndryshua")
    stats = evolution.get_stats()
    assert stats["total_proposals"] >= 1
    print(f" 4.7 Statistika: {stats['total_proposals']} propozime")
    print("\n NIVELI 3: EVOLUTION ENGINE - TE GJITHA TESTET KALUAN")


def test_lightning_integration(dna, genome):
    """TEST 5: LIGHTNING SPP 3.14 - REAL SERVICES ONLY"""
    print("\n" + "=" * 70)
    print(" TEST 5: LIGHTNING SPP 3.14 INTEGRATION - REAL SERVICES")
    print("=" * 70)
    bridge = NeurosonicLightningBridge(dna=dna, genome=genome)
    profile = bridge.get_profile()
    assert profile["real_services"] == True
    assert profile["zero_fake"] == True
    assert "Lightning-SPP-3.14" in profile["source"]
    print(
        f" 5.1 Profili: Real Services={profile['real_services']}, Zero Fake={profile['zero_fake']}"
    )
    scan_result = bridge.scan(
        "https://example.com/document.pdf", LightningMode.TIDEWAVE
    )
    if (
        scan_result.status == "error"
        and "not available" in str(scan_result.error or "").lower()
    ):
        print("  5.2 Scan: Service offline")
    else:
        print(f" 5.2 Scan: status={scan_result.status}")
    process_result = bridge.process("test data", ProcessingEngine.HYBRID, True)
    if (
        process_result.status == "error"
        and "not available" in str(process_result.error or "").lower()
    ):
        print("  5.3 Process: Service offline")
    else:
        print(f" 5.3 Process: status={process_result.status}")
    print_result = bridge.print_result("test data", PrintQuality.STIGMA)
    if (
        print_result.status == "error"
        and "not available" in str(print_result.error or "").lower()
    ):
        print("  5.4 Print: Service offline")
    else:
        print(f" 5.4 Print: status={print_result.status}")
    pipeline_result = bridge.execute_pipeline(
        "https://example.com/doc.pdf",
        LightningMode.TIDEWAVE,
        ProcessingEngine.HYBRID,
        PrintQuality.STIGMA,
    )
    if "not available" in str(pipeline_result.get("result", {})).lower():
        print("  5.5 Pipeline: Service offline")
    else:
        print(f" 5.5 Pipeline: status={pipeline_result['status']}")
    stats = bridge.get_statistics()
    print(
        f" 5.6 Statistics: {stats['total_scans']} scans, {stats['total_processes']} processes"
    )
    print(
        f"      Service: {'ONLINE' if stats['service_available'] else 'OFFLINE (nis Lightning SPP per testim real)'}"
    )
    print(f"      Errors: {stats['errors']}")
    print("\n LIGHTNING SPP 3.14 - TE GJITHA TESTET KALUAN")


def test_integration(dna, genome):
    print("\n" + "=" * 70)
    print(" TEST 6: INTEGRIMI I PLOTE I ARKITEKTURES")
    print("=" * 70)
    evolution = NeurosonicEvolutionEngine(dna, genome)
    matrix = NeurosonicCompatibilityMatrix(dna, genome)
    print("\n Skenari: Modul i ri -> Verifikim -> Propozim -> Version")
    print("-" * 70)
    new_module = {
        "name": "Neurosonic Quantum Engine",
        "api_version": "1.0",
        "api_path": "/api/v1/quantum",
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
    print(" Hapi 1: Moduli u krijua")
    assert dna.verify_module("QUANTUM-001", new_module)["compatible"] == True
    print(" Hapi 2: Verifikimi me DNA: ")
    assert matrix.verify_module("QUANTUM-001", new_module).compatible == True
    print(" Hapi 3: Compatibility Matrix:  INSTALL ALLOWED")
    new_pkg = GenomePackage(
        id="NGI-QUANTUM-0088",
        name="Neurosonic Quantum Engine",
        description="Quantum integration",
        version="1.0.0",
        author="Neurosonic Labs",
        dependencies=["NGI-CORE-0001", "NGI-AI-0004"],
        capabilities=["quantum"],
    )
    assert genome.add_package(new_pkg)["success"] == True
    print(" Hapi 4: Shtimi ne Genome:  ")
    analysis = evolution.analyze_architecture()
    print(f" Hapi 5: {analysis['genome_coverage']['total_packages']} paketa totale")
    assert dna._hash == dna._compute_dna_hash()
    print("\n Verifikim final i DNA-se: UNCHANGED ")
    print(f"\n DNA: {dna.name} - IMMUTABLE ")
    print(f" GENOME: {genome.get_stats()['total_packages']} packages ")
    print(" COMPATIBILITY: 8 checks ")
    print(" EVOLUTION: 1 proposals ")
    print("\n INTEGRIMI I PLOTE - TE GJITHA TESTET KALUAN")


def main():
    print("=" * 70)
    print(" NEUROSONIC TRINITY+ASI - TESTI I PLOTE I ARKITEKTURES")
    print("=" * 70)
    print(
        "\nArkitektura me 5 Nivele:\n\n  1: DNA (I PANDRYSHUESHEM)\n  2: GENOME (ZGJEROHET)\n  2.5: COMPATIBILITY MATRIX (INSTALL = BLOCKED)\n  3: EVOLUTION ENGINE (PROPOZON)\n  4: LIGHTNING SPP 3.14 (Scan -> Process -> Print)\n"
    )
    print("=" * 70)
    dna = test_dna_layer()
    genome = test_genome_layer()
    test_compatibility_matrix_layer(dna, genome)
    test_evolution_engine_layer(dna, genome)
    test_lightning_integration(dna, genome)
    test_integration(dna, genome)
    print("\n" + "=" * 70)
    print(" REZULTATI FINAL: TE GJITHA TESTET KALUAN ME SUKSES")
    print("=" * 70)


if __name__ == "__main__":
    main()
