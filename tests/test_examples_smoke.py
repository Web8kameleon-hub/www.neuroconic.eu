import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_basic_usage_example_runs() -> None:
    script = ROOT / "examples" / "basic_usage.py"
    completed = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=True,
    )

    assert "Neurosonic Public Example" in completed.stdout
    assert "Compatible: True" in completed.stdout
