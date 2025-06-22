import subprocess
import sys
from pathlib import Path


def test_main_output(tmp_path: Path) -> None:
    """Call the CLI module and verify the output and created structure."""
    result = subprocess.run(
        [sys.executable, "-m", "project_generator.main", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Hello from project_generator" in result.stdout
    assert (tmp_path / "src").exists()
