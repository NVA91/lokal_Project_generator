from pathlib import Path
import shutil

from src.vscode_integration import VSCodeIntegration


def test_setup(tmp_path):
    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    vscode = VSCodeIntegration(project_dir)
    vscode.setup()
    settings = project_dir / ".vscode" / "settings.json"
    tasks = project_dir / ".vscode" / "tasks.json"
    assert settings.exists()
    assert tasks.exists()
    # cleanup
    shutil.rmtree(project_dir / ".vscode")
