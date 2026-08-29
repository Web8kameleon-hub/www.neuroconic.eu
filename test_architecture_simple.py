#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST I PLOTE I ARKITEKTURES NEUROSONIC
DNA + GENOME + COMPATIBILITY + EVOLUTION
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from neurosonic_dna import NeurosonicDNA
from neurosonic_genome import NeurosonicGenome
from neurosonic_compatibility import NeurosonicCompatibilityMatrix
from neurosonic_evolution import NeurosonicEvolutionEngine


def test_dna():
    """Test DNA layer"""
    print("\n" + "=" * 70)
    print("TEST 1: DNA - I PANDRYSHU ESHM")
    print("=" * 70)
    
    dna = NeurosonicDNA()
    assert dna.immutable == True
    print("OK 1.1 - DNA initialized")
    
    rules = dna.get_all_rules()
    assert len(rules["constitution"]) == 10
    print("OK 1.2 - Constitution has 10 laws")
    
    stats = dna.get_stats()
    print(f"OK 1.3 - Stats: {stats['total_rules']} total rules")
    
    return dna


def test_genome():
    """Test GENOME layer"""
    print("\n" + "=" * 70)
    print("TEST 2: GENOME - ZGJEROHET")
    print("=" * 70)
    
    genome = NeurosonicGenome()
    packages = genome.list_packages()
    print(f"OK 2.1 - {len(packages)} packages")
    
    stats = genome.get_stats()
    print(f"OK 2.2 - Genome stats: {stats}")
    
    return genome


def test_compatibility(dna, genome):
    """Test COMPATIBILITY MATRIX"""
    print("\n" + "=" * 70)
    print("TEST 3: COMPATIBILITY MATRIX")
    print("=" * 70)
    
    matrix = NeurosonicCompatibilityMatrix(dna, genome)
    
    # Test compatible module
    good_config = {
        "constitution_compatibility": ["G001", "G002", "G003", "G004", "G005", "G006", "G007", "G008", "G009", "G010"],
        "security_compatibility": ["SR001", "SR002", "SR003", "SR004", "SR005", "SR006", "SR007", "SR008"],
        "data_compatibility": ["DR001", "DR002", "DR003", "DR004", "DR005"],
        "api_compatibility": ["AR001", "AR002", "AR003", "AR004"],
    }
    result = matrix.verify_module("TEST-001", good_config)
    assert result.compatible == True
    print("OK 3.1 - Compatible module verified")
    
    # Test incompatible module
    bad_config = {"constitution_compatibility": []}
    result = matrix.verify_module("TEST-002", bad_config)
    assert result.compatible == False
    print("OK 3.2 - Incompatible module blocked")
    
    return matrix


def test_evolution(dna, genome):
    """Test EVOLUTION ENGINE"""
    print("\n" + "=" * 70)
    print("TEST 4: EVOLUTION ENGINE")
    print("=" * 70)
    
    evolution = NeurosonicEvolutionEngine(dna, genome)
    
    analysis = evolution.analyze_architecture()
    print(f"OK 4.1 - Architecture analyzed: {analysis['status']}")
    
    proposal = evolution.propose_new_rule(
        description="Test rule for testing",
        category="governance",
        impact_level="low"
    )
    print(f"OK 4.2 - Proposal created: {proposal['proposal_id']}")
    
    stats = evolution.get_stats()
    print(f"OK 4.3 - Evolution stats: {stats}")
    
    return evolution


def main():
    """Main test runner"""
    print("=" * 70)
    print("NEUROSONIC TRINITY+ASI - TEST SUITE")
    print("=" * 70)
    
    tests_passed = 0
    tests_failed = 0
    
    try:
        dna = test_dna()
        tests_passed += 1
    except Exception as e:
        print(f"FAILED: DNA - {e}")
        tests_failed += 1
        return
    
    try:
        genome = test_genome()
        tests_passed += 1
    except Exception as e:
        print(f"FAILED: GENOME - {e}")
        tests_failed += 1
        return
    
    try:
        matrix = test_compatibility(dna, genome)
        tests_passed += 1
    except Exception as e:
        print(f"FAILED: COMPATIBILITY - {e}")
        tests_failed += 1
    
    try:
        evolution = test_evolution(dna, genome)
        tests_passed += 1
    except Exception as e:
        print(f"FAILED: EVOLUTION - {e}")
        tests_failed += 1
    
    # Final report
    print("\n" + "=" * 70)
    print("REZULTATI FINAL")
    print("=" * 70)
    print(f"Kaluan: {tests_passed}")
    print(f"Deshtuan: {tests_failed}")
    print(f"Perqindja: {tests_passed * 100 / (tests_passed + tests_failed):.0f}%")
    print("=" * 70)
    
    if tests_failed == 0:
        print("\nTE GJITHA TESTET KALUAN!")
        return 0
    else:
        print(f"\n{tests_failed} TESTE DESHTUAN")
        return 1


if __name__ == "__main__":
    sys.exit(main())
