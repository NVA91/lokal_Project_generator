from __future__ import annotations

"""Helpers for configuring VS Code settings for a project."""

from pathlib import Path
import json


class VSCodeIntegration:
    """Create VS Code configuration files for a project."""

    SETTINGS = {
        "python.pythonPath": ".venv/bin/python",
        "files.watcherExclude": {"**/.venv/**": True, "**/__pycache__/**": True},
        "search.exclude": {"**/.venv/**": True, "**/__pycache__/**": True},
        "editor.renderLineHighlight": "gutter",
    }

    TASKS = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Setup Python Environment",
                "type": "shell",
                "command": "python -m venv .venv && source .venv/bin/activate && pip install -r requirements-dev.txt",
                "presentation": {"reveal": "always", "panel": "new"},
            }
        ],
    }

    def __init__(self, project_dir: Path) -> None:
        self.project_dir = Path(project_dir)
        self.vscode_dir = self.project_dir / ".vscode"

    def setup(self) -> None:
        """Write settings.json and tasks.json into the .vscode directory."""
        self.vscode_dir.mkdir(exist_ok=True)
        settings_path = self.vscode_dir / "settings.json"
        tasks_path = self.vscode_dir / "tasks.json"
        if not settings_path.exists():
            settings_path.write_text(json.dumps(self.SETTINGS, indent=2))
        if not tasks_path.exists():
            tasks_path.write_text(json.dumps(self.TASKS, indent=2))
