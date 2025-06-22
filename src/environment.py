from __future__ import annotations

"""Utilities for managing a virtual environment."""

from pathlib import Path
import subprocess
import sys
import os
from typing import Iterable


class VirtualEnvironmentManager:
    """Manage creation and package installation for a virtual environment."""

    def __init__(self, project_dir: Path) -> None:
        self.project_dir = Path(project_dir)
        self.venv_dir = self.project_dir / ".venv"

    def create(self) -> None:
        """Create the virtual environment if it doesn't exist."""
        if not self.venv_dir.exists():
            subprocess.run([
                sys.executable,
                "-m",
                "venv",
                str(self.venv_dir),
            ], check=True)

    def install(self, requirements_files: Iterable[Path]) -> None:
        """Install dependencies from the given requirement files."""
        if not self.venv_dir.exists():
            self.create()
        scripts_dir = "Scripts" if os.name == "nt" else "bin"
        pip = self.venv_dir / scripts_dir / "pip"
        for req in requirements_files:
            if req.exists():
                subprocess.run([
                    str(pip),
                    "install",
                    "-r",
                    str(req),
                ], check=True)


