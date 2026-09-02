import json
from pathlib import Path

from neurosonic_compatibility import NeurosonicCompatibilityMatrix
from neurosonic_dna import NeurosonicDNA
from neurosonic_genome import NeurosonicGenome


ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "samples"


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def test_valid_sample_is_compatible() -> None:
    dna = NeurosonicDNA()
    genome = NeurosonicGenome()
    matrix = NeurosonicCompatibilityMatrix(dna, genome)

    config = _load_json(SAMPLES / "module_config_valid.json")
    result = matrix.verify_module("PUBLIC-VALID-001", config)

    assert result.compatible is True
    assert result.score >= 75


def test_invalid_sample_is_blocked() -> None:
    dna = NeurosonicDNA()
    genome = NeurosonicGenome()
    matrix = NeurosonicCompatibilityMatrix(dna, genome)

    config = _load_json(SAMPLES / "module_config_invalid.json")
    result = matrix.verify_module("PUBLIC-INVALID-001", config)

    assert result.compatible is False
    assert len(result.violations) > 0
