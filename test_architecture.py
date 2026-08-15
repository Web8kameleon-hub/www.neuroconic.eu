#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST I PLOTE I ARKITEKTURES SE RE NEUROSONIC
DNA + GENOME + COMPATIBILITY MATRIX + EVOLUTION ENGINE

Nese deshton: INSTALL = BLOCKED
"""

import sys
import os

# Shto direktorine aktuale ne path per importe
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from neurosonic_dna import NeurosonicDNA
from neurosonic_genome import NeurosonicGenome, GenomePackage
from neurosonic_compatibility import NeurosonicCompatibilityMatrix
from neurosonic_evolution import NeurosonicEvolutionEngine


def test_dna_layer():
 """Test per NIVELI 1: DNA"""
 print("\n" + "=" * 70)
 print(" TEST 1: DNA - I PANDrySHUESHeM")
 print("=" * 70)

 dna = NeurosonicDNA()

 # Test 1.1: Verifiko qe DNA eshte inicializuar
 assert dna.name == "Neurosonic DNA v1.0", "DNA name mismatch"
 assert dna.immutable == True, "DNA must be immutable"
 print(" 1.1 DNA inicializuar sakte")

 # Test 1.2: Verifiko numrin e rregullave
 rules = dna.get_all_rules()
 assert len(rules["constitution"]) == 10, (
 f"Expected 10 constitution laws, got {len(rules['constitution'])}"
 )
 assert len(rules["security"]) == 8, (
 f"Expected 8 security rules, got {len(rules['security'])}"
 )
 assert len(rules["data"]) == 5, f"Expected 5 data rules, got {len(rules['data'])}"
 assert len(rules["api"]) == 4, f"Expected 4 API rules, got {len(rules['api'])}"
 assert len(rules["memory"]) == 6, (
 f"Expected 6 memory rules, got {len(rules['memory'])}"
 )
 assert len(rules["governance"]) == 6, (
 f"Expected 6 governance rules, got {len(rules['governance'])}"
 )
 assert len(rules["quality"]) == 5, (
 f"Expected 5 quality rules, got {len(rules['quality'])}"
 )
 assert len(rules["core_values"]) == 6, (
 f"Expected 6 core values, got {len(rules['core_values'])}"
 )
 print(" 1.2 Te gjitha rregullat jane te pranishme")

 # Test 1.3: Verifiko hash-in e integritetit
 initial_hash = dna._hash
 recomputed_hash = dna._compute_dna_hash()
 assert initial_hash == recomputed_hash, "DNA hash integrity check failed"
 print(f" 1.3 DNA hash integrity: {initial_hash}")

 # Test 1.4: Verifiko modul te perputhshem
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
 result = dna.verify_module("MOD-001", good_module)
 assert result["compatible"] == True, "Good module should be compatible"
 print(" 1.4 Modul i perputhshem u verifikua sakte")

 # Test 1.5: Verifiko modul te paperputhshem
 bad_module = {
 "constitution_compatibility": [],
 "security_compatibility": [],
 }
 result = dna.verify_module("MOD-002", bad_module)
 assert result["compatible"] == False, "Bad module should NOT be compatible"
 assert len(result["violations"]) > 0, "Bad module should have violations"
 print(" 1.5 Modul i paperputhshem u bllokua sakte")

 # Test 1.6: Verifiko Kushtetuten per veprime
 assert dna.verify_constitution_action("send_to_external", "module") == False, (
 "External send without module should fail"
 )
 assert dna.verify_constitution_action("send_to_external", "api_public") == True, (
 "API public should be allowed"
 )
 assert dna.verify_constitution_action("delete_user_data", "user_self") == True, (
 "User self-delete should be allowed"
 )
 assert dna.verify_constitution_action("send_unencrypted", "module") == False, (
 "Unencrypted send should fail"
 )
 print(" 1.6 Kushtetuta zbaton rregullat sakte")

 # Test 1.7: Verifiko statistikat
 stats = dna.get_stats()
 assert stats["total_rules"] > 40, (
 f"Expected >40 total rules, got {stats['total_rules']}"
 )
 print(f" 1.7 Statistika: {stats['total_rules']} rregulla gjithsej")

 print("\n" + "=" * 70)
 print(" NIVELI 1: DNA - TE GJITHA TESTET KALUAN")
 print("=" * 70)
 return dna


def test_genome_layer():
 """Test per NIVELI 2: GENOME"""
 print("\n" + "=" * 70)
 print(" TEST 2: GENOME - ZGJEROHET")
 print("=" * 70)

 genome = NeurosonicGenome()

 # Test 2.1: Verifiko paketat themelore
 assert len(genome.packages) >= 17, (
 f"Expected >=17 core packages, got {len(genome.packages)}"
 )
 print(f" 2.1 {len(genome.packages)} paketa themelore")

 # Test 2.2: Verifiko indekset NGI
 assert "NGI-CORE-0001" in genome.packages, "Missing CLX Kernel"
 assert "NGI-AI-0004" in genome.packages, "Missing CLX LLM"
 assert "NGI-MEM-0002" in genome.packages, "Missing HVO Memory"
 assert "NGI-SEC-0012" in genome.packages, "Missing Security Fabric"
 print(" 2.2 Indekset NGI jane te plota")

 # Test 2.3: Verifiko marrjen e paketes
 pkg = genome.get_package("NGI-CORE-0001")
 assert pkg["name"] == "CLX Kernel", f"Expected CLX Kernel, got {pkg['name']}"
 assert pkg["version"] == "1.0.0", f"Expected v1.0.0, got {pkg['version']}"
 print(" 2.3 Marrja e paketes funksionon")

 # Test 2.4: Verifiko shtimin e paketes se re
 new_pkg = GenomePackage(
 id="NGI-TEST-9999",
 name="Test Package",
 description="Test package for verification",
 version="1.0.0",
 author="Neurosonic Test",
 dependencies=["NGI-CORE-0001"],
 capabilities=["test_capability"],
 )
 result = genome.add_package(new_pkg)
 assert result["success"] == True, f"Add package failed: {result['message']}"
 print(f" 2.4 Paketa e re u shtua: {result['message']}")

 # Test 2.5: Verifiko pamundesine e shtimit te paketes me varesi qe mungon
 bad_pkg = GenomePackage(
 id="NGI-TEST-9998",
 name="Bad Test",
 description="Package with missing dependency",
 version="1.0.0",
 author="Neurosonic Test",
 dependencies=["NGI-NONEXIST-9999"],
 capabilities=["test"],
 )
 result = genome.add_package(bad_pkg)
 assert result["success"] == False, "Should not add package with missing dependency"
 print(f" 2.5 Paketa me varesi qe mungon u bllokua: {result['message']}")

 # Test 2.6: Verifiko kategorizimin
 categories = genome.get_packages_by_category()
 assert len(categories["core"]) >= 3, (
 f"Expected >=3 core packages, got {len(categories['core'])}"
 )
 assert len(categories["ai"]) >= 2, (
 f"Expected >=2 AI packages, got {len(categories['ai'])}"
 )
 print(" 2.6 Kategorizimi i paketave funksionon")

 # Test 2.7: Verifiko heqjen e paketes
 result = genome.remove_package("NGI-TEST-9999")
 assert result["success"] == True, f"Remove package failed: {result['message']}"
 print(f" 2.7 Paketa u hoq: {result['message']}")

 # Test 2.8: Verifiko pamundesine e heqjes se paketes qe ka varesi
 result = genome.remove_package("NGI-CORE-0001")
 assert result["success"] == False, "Should not remove package with dependencies"
 print(f" 2.8 Paketa me varesi nuk u hoq: {result['message']}")

 # Test 2.9: Verifiko statistikat
 stats = genome.get_stats()
 assert stats["total_packages"] >= 17, (
 f"Expected >=17 packages, got {stats['total_packages']}"
 )
 print(f" 2.9 Statistika: {stats['total_packages']} paketa")

 print("\n" + "=" * 70)
 print(" NIVELI 2: GENOME - TE GJITHA TESTET KALUAN")
 print("=" * 70)
 return genome


def test_compatibility_matrix_layer(dna, genome):
 """Test per NIVELI 2.5: COMPATIBILITY MATRIX"""
 print("\n" + "=" * 70)
 print(" TEST 3: COMPATIBILITY MATRIX - INSTALL = BLOCKED")
 print("=" * 70)

 matrix = NeurosonicCompatibilityMatrix(dna, genome)

 # Test 3.1: Verifiko modul te perputhshem
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
 assert result.compatible == True, "Good module should be compatible"
 assert len(result.violations) == 0, (
 f"Good module should have 0 violations, got {len(result.violations)}"
 )
 print(" 3.1 Modul i perputhshem: INSTALL ALLOWED")

 # Test 3.2: Verifiko modul te paperputhshem
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
 assert result.compatible == False, "Bad module should NOT be compatible"
 assert len(result.violations) > 0, "Bad module should have violations"
 print(" 3.2 Modul i paperputhshem: INSTALL = BLOCKED")

 # Test 3.3: Verifiko te gjitha kontrollet jane ekzekutuar
 good_result = matrix.verify_module("MOD-003", good_module)
 expected_checks = [
 "constitution_compatibility",
 "genome_compatibility",
 "api_compatibility",
 "memory_compatibility",
 "security_compatibility",
 "performance_compatibility",
 "license_compatibility",
 "data_compatibility",
 ]
 for check in expected_checks:
 assert check in good_result.checks, f"Missing check: {check}"
 assert all(good_result.checks.values()), "All checks should pass for good module"
 print(" 3.3 Te 8 kontrollet jane ekzekutuar")

 # Test 3.4: Verifiko raportin
 report = matrix.generate_report(good_result)
 assert "INSTALL ALLOWED" in report, "Report should show INSTALL ALLOWED"
 print(" 3.4 Raporti i perputhshmerise funksionon")

 print("\n" + "=" * 70)
 print(" NIVELI 2.5: COMPATIBILITY MATRIX - TE GJITHA TESTET KALUAN")
 print("=" * 70)


def test_evolution_engine_layer(dna, genome):
 """Test per NIVELI 3: EVOLUTION ENGINE"""
 print("\n" + "=" * 70)
 print(" TEST 4: EVOLUTION ENGINE - PROPOZON, NUK NDRYSHON")
 print("=" * 70)

 evolution = NeurosonicEvolutionEngine(dna, genome)

 # Test 4.1: Verifiko analizen e arkitektures
 analysis = evolution.analyze_architecture()
 assert "dna_integrity" in analysis, "Missing dna_integrity"
 assert "genome_coverage" in analysis, "Missing genome_coverage"
 assert "potential_conflicts" in analysis, "Missing potential_conflicts"
 assert "optimization_suggestions" in analysis, "Missing optimization_suggestions"
 assert analysis["dna_integrity"] == True, "DNA integrity should be True"
 print(f" 4.1 Analiza e arkitektures: DNA Integrity = {analysis['dna_integrity']}")

 # Test 4.2: Verifiko mbulimin e genome-se
 coverage = analysis["genome_coverage"]
 assert coverage["coverage_percent"] >= 80, (
 f"Coverage should be >=80%, got {coverage['coverage_percent']}"
 )
 print(f" 4.2 Mbulimi i Genome-se: {coverage['coverage_percent']:.0f}%")

 # Test 4.3: Verifiko propozimin e rregullit te ri
 proposal = evolution.propose_new_rule(
 "All AI responses must be verified by at least 3 independent sources before output",
 category="governance",
 impact_level="high",
 )
 assert "id" in proposal, "Missing proposal id"
 assert proposal["status"] == "proposed", (
 f"Expected 'proposed', got {proposal['status']}"
 )
 assert "analysis" in proposal, "Missing proposal analysis"
 print(
 f" 4.3 Propozimi {proposal['id']} u krijua: '{proposal['description'][:50]}...'"
 )

 # Test 4.4: Verifiko analizen e propozimit
 analysis_data = proposal["analysis"]
 assert "feasibility" in analysis_data, "Missing feasibility"
 assert "impact" in analysis_data, "Missing impact"
 assert "dna_impact" in analysis_data, "Missing dna_impact"
 print(
 f" 4.4 Analiza e propozimit: feasibility={analysis_data['feasibility'] * 100:.0f}%, dna_impact={analysis_data['dna_impact']}"
 )

 # Test 4.5: Verifiko krijimin e versionit te ri
 version = evolution.create_new_version(
 {
 "add": ["Quantum Package", "Robotics Package"],
 "update": ["CLX Kernel to v2.0"],
 }
 )
 assert "version" in version, "Missing version number"
 assert "analysis" in version, "Missing version analysis"
 # Shtimi/update i paketave nuk prek DNA-ne, pra governance approval nuk kerkohet
 print(
 f" 4.5 Versioni {version['version']} u krijua (Governance Approval: {version['requires_governance_approval']}, Human Override: {version['requires_human_override']})"
 )

 # Test 4.6: Verifiko qe DNA nuk ndryshon
 current_hash = dna._hash
 recomputed_hash = dna._compute_dna_hash()
 assert current_hash == recomputed_hash, (
 "DNA should NOT change after evolution operations"
 )
 print(f" 4.6 DNA nuk u ndryshua: hash={current_hash}")

 # Test 4.7: Verifiko statistikat
 stats = evolution.get_stats()
 assert stats["total_proposals"] >= 1, "Should have at least 1 proposal"
 assert stats["total_analyses"] >= 1, "Should have at least 1 analysis"
 print(
 f" 4.7 Statistika: {stats['total_proposals']} propozime, {stats['total_analyses']} analiza"
 )

 print("\n" + "=" * 70)
 print(" NIVELI 3: EVOLUTION ENGINE - TE GJITHA TESTET KALUAN")
 print("=" * 70)


def test_integration(dna, genome):
 """Test i integrimit te te gjitha niveleve"""
 print("\n" + "=" * 70)
 print(" TEST 5: INTEGRIMI I PLOTE I ARKITEKTURES")
 print("=" * 70)

 evolution = NeurosonicEvolutionEngine(dna, genome)
 matrix = NeurosonicCompatibilityMatrix(dna, genome)

 # 5.1: DNA -> Module verification -> Evolution cycle
 print("\n Skenari: Modul i ri -> Verifikim -> Propozim -> Version")
 print("-" * 70)

 # Hapi 1: Krijo modul
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

 # Hapi 2: Verifiko me DNA
 dna_check = dna.verify_module("QUANTUM-001", new_module)
 assert dna_check["compatible"] == True, "Module should be DNA compatible"
 print(" Hapi 2: Verifikimi me DNA: ")

 # Hapi 3: Verifiko me Compatibility Matrix
 matrix_check = matrix.verify_module("QUANTUM-001", new_module)
 assert matrix_check.compatible == True, "Module should pass compatibility"
 print(" Hapi 3: Compatibility Matrix: INSTALL ALLOWED")

 # Hapi 4: Shto ne Genome
 new_genome_pkg = GenomePackage(
 id="NGI-QUANTUM-0088",
 name="Neurosonic Quantum Engine",
 description="Quantum computing integration for Neurosonic",
 version="1.0.0",
 author="Neurosonic Labs",
 dependencies=["NGI-CORE-0001", "NGI-AI-0004"],
 capabilities=["quantum_simulation", "quantum_crypto"],
 )
 add_result = genome.add_package(new_genome_pkg)
 assert add_result["success"] == True, f"Add failed: {add_result['message']}"
 print(f" Hapi 4: Shtimi ne Genome: {add_result['message']}")

 # Hapi 5: Analizo arkitekturen pas ndryshimit
 analysis = evolution.analyze_architecture()
 print(
 f" Hapi 5: Analiza pas ndryshimit: {analysis['genome_coverage']['total_packages']} paketa totale"
 )

 # Hapi 6: Propozo rregull te ri nese nevojitet
 if analysis["potential_conflicts"]:
 print(f" Hapi 6: U gjeten {len(analysis['potential_conflicts'])} konflikte")
 for conflict in analysis["potential_conflicts"]:
 print(f" Propozohet rregull per: {conflict['description']}")
 else:
 print(" Hapi 6: Nuk u gjeten konflikte")

 # Hapi 7: Krijo version te ri
 version = evolution.create_new_version(
 {
 "add": ["Neurosonic Quantum Engine"],
 }
 )
 print(f" Hapi 7: Versioni {version['version']} u krijua")

 # 5.2: Verifiko qe DNA nuk ndryshoi gjate gjithe ciklit
 final_hash = dna._hash
 print(f"\n Verifikim final i DNA-se: hash={final_hash}")
 assert final_hash == dna._compute_dna_hash(), "DNA must not change during lifecycle"

 # 5.3: Permbledhje
 print("\n PERMBLEDHJE E ARKITEKTURES:")
 print("-" * 70)
 print(f" DNA: {dna.name} - IMMUTABLE ")
 print(f" GENOME: {genome.get_stats()['total_packages']} packages ")
 print(f" COMPATIBILITY: {len(matrix.checks)} checks ")
 print(
 f" EVOLUTION: {len(evolution.proposals)} proposals, {len(evolution.analysis_history)} analyses "
 )
 print(f" DNA INTEGRITY: UNCHANGED ")

 print("\n" + "=" * 70)
 print(" INTEGRIMI I PLOTE - TE GJITHA TESTET KALUAN")
 print("=" * 70)


def main():
 """Main test runner"""
 print("=" * 70)
 print(" NEUROSONIC TRINITY+ASI - TESTI I PLOTE I ARKITEKTURES")
 print("=" * 70)
 print("""
 Arkitektura me 3 Nivele:
 
 NIVELI 1: DNA (I PANDrySHUESHeM)
 Kushtetuta, Siguria, Data, API, Memory, Qeverisja
 
 NIVELI 2: GENOME (ZGJEROHET)
 Paketat qe shtojne aftesi pa prekur DNA-ne
 
 NIVELI 2.5: COMPATIBILITY MATRIX
 Nese deshton: INSTALL = BLOCKED
 
 NIVELI 3: EVOLUTION ENGINE (PROPOZON)
 Analizon, zbulon konflikte, propozon, nuk ndryshon DNA
 """)
 print("=" * 70)

 # Ekzekuto testet
 dna = test_dna_layer()
 genome = test_genome_layer()
 test_compatibility_matrix_layer(dna, genome)
 test_evolution_engine_layer(dna, genome)
 test_integration(dna, genome)

 # Rezultati final
 print("\n" + "=" * 70)
 print(" REZULTATI FINAL: TE GJITHA TESTET KALUAN ME sukses")
 print("=" * 70)
 print("""
 
 NEUROSONIC TRINITY+ASI - ARKITEKTURA E RE 
 
 DNA: 10 ligje + 43 rregulla - IMMUTABLE 
 GENOME: 17+ paketa - ZGJERUESHEM 
 COMPATIBILITY: 8 kontrolle - INSTALL = BLOCKED 
 EVOLUTION: PROPOZON, NUK NDRYSHON DNA 
 
 NGI (Neurosonic Genome Index) 
 - NGI-CORE-0001: CLX Kernel 
 - NGI-AI-0004: CLX LLM 
 - NGI-MEM-0002: HVO Memory 
 - NGI-AGENT-0045: Research Agent 
 - NGI-SEC-0012: Security Fabric 
 
 INSTALL ALLOWED VETEM NESE: 
 - Perputhet me Kushtetuten (10 ligjet) 
 - Respekton sigurine (8 rregulla) 
 - Perdor CUDM per te dhenat 
 - Ka kriptim dhe Zero Trust 
 - Ka SSE dhe Tide compatibility 
 - Licenca eshte e lejuar 
 
 """)


if __name__ == "__main__":
 main()
