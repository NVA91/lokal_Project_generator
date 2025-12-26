import subprocess
from pathlib import Path


def run_setup_script(tmp_path):
    script = (
        Path(__file__).resolve().parents[1] / "setup_project.sh"
    )
    result = subprocess.run(
        ["sh", script], cwd=tmp_path, capture_output=True, text=True
    )
    return result


def test_setup_project_creates_structure(tmp_path):
    result = run_setup_script(tmp_path)
    assert result.returncode == 0, result.stderr
    for dirname in ["src", "tests", "docs", "venv"]:
        assert (tmp_path / dirname).exists()


def test_setup_project_idempotent(tmp_path):
    first = run_setup_script(tmp_path)
    second = run_setup_script(tmp_path)
    assert first.returncode == 0
    assert second.returncode == 0
