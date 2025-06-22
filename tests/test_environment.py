from pathlib import Path
import shutil

from src.environment import VirtualEnvironmentManager


def test_create_venv(tmp_path):
    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    manager = VirtualEnvironmentManager(project_dir)
    manager.create()
    assert (project_dir / ".venv").exists()
    # cleanup to save space
    shutil.rmtree(project_dir / ".venv")
