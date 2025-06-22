"""Utility for creating Python virtual environments."""

from __future__ import annotations

import asyncio
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Callable, Optional
from logging import Logger


class VirtualEnvironmentManager:
    """Manages creation of virtual environments."""

    def __init__(self, logger: Logger, progress_callback: Optional[Callable[[str], None]] = None):
        self.logger = logger
        self.progress_callback = progress_callback

    async def create_venv(self, project_path: Path) -> bool:
        """Create a virtual environment in the given project path.

        Returns True if creation succeeded or already exists, False otherwise.
        """
        venv_path = project_path / ".venv"
        try:
            if not self._validate_python_venv():
                raise EnvironmentError("Python venv module not available")

            if venv_path.exists():
                self.logger.warning("venv already exists: %s", venv_path)
                return True

            if self.progress_callback:
                self.progress_callback("Creating virtual environment...")

            process = await asyncio.create_subprocess_exec(
                sys.executable,
                "-m",
                "venv",
                str(venv_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, "venv", stderr)

            self.logger.info("Virtual environment created at %s", venv_path)
            if self.progress_callback:
                self.progress_callback("Virtual environment ready")
            return True
        except Exception as exc:
            self.logger.error("venv creation failed: %s", exc)
            if venv_path.exists():
                shutil.rmtree(venv_path)
            return False

    def _validate_python_venv(self) -> bool:
        """Return True if venv module is available."""
        try:
            import venv  # noqa: F401

            return True
        except ImportError:
            return False
