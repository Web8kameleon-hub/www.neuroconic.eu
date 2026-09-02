#!/usr/bin/env python3
"""Public example: basic Neurosonic usage without external dependencies."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from neurosonic_compatibility import NeurosonicCompatibilityMatrix
from neurosonic_dna import NeurosonicDNA
from neurosonic_genome import NeurosonicGenome


def main() -> None:
    dna = NeurosonicDNA()
    genome = NeurosonicGenome()
    matrix = NeurosonicCompatibilityMatrix(dna, genome)

    module_config = {
        "name": "Public Demo Module",
        "api_version": "v1",
        "api_path": "/api/demo",
        "memory_type": "HVO",
        "encryption": "AES256",
        "zero_trust": True,
        "sse_support": True,
        "tide_compatible": True,
        "cudm_compatible": True,
        "license": "Neurosonic",
        "dependencies": ["NGI-CORE-0001"],
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

    result = matrix.verify_module("DEMO-PUBLIC-001", module_config)
    print("=== Neurosonic Public Example ===")
    print(f"Compatible: {result.compatible}")
    print(f"Score: {result.score:.1f}%")
    print(f"Violations: {len(result.violations)}")


if __name__ == "__main__":
    main()
