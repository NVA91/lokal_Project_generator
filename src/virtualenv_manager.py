from __future__ import annotations

import asyncio
import os
import shutil
import subprocess
import sys
from logging import Logger
from pathlib import Path
from typing import Callable, Optional


class VirtualEnvironmentManager:
    """Utility to create and validate Python virtual environments."""

    def __init__(self, logger: Logger, progress_callback: Optional[Callable[[str], None]] = None) -> None:
        self.logger = logger
        self.progress_callback = progress_callback

    async def create_venv(self, project_path: Path) -> bool:
        """Create a virtual environment inside ``project_path``.

        Parameters
        ----------
        project_path:
            Directory where the ``.venv`` folder will be created.

        Returns
        -------
        bool
            ``True`` if the environment was created or already exists,
            otherwise ``False`` on failure.
        """
        venv_path = project_path / ".venv"
        try:
            if not self._validate_python_venv():
                raise EnvironmentError("Python venv module not available")

            if venv_path.exists():
                self.logger.warning("virtual environment already exists: %s", venv_path)
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
                raise subprocess.CalledProcessError(process.returncode, "venv", stderr.decode())

            if stdout:
                self.logger.debug(stdout.decode())
            self.logger.info("Virtual environment created at %s", venv_path)
            return True
        except Exception as exc:
            self.logger.error("venv creation failed: %s", exc)
            if venv_path.exists():
                shutil.rmtree(venv_path)
            return False

    async def install_dependencies(self, project_path: Path, requirements_file: Path) -> bool:
        """Install dependencies from ``requirements_file`` into the virtual environment.

        Parameters
        ----------
        project_path:
            Directory containing the virtual environment.
        requirements_file:
            ``requirements.txt`` file with packages to install.

        Returns
        -------
        bool
            ``True`` if the installation succeeded or the file is missing,
            otherwise ``False``.
        """
        venv_path = project_path / ".venv"
        python_exe = venv_path / ("Scripts" if os.name == "nt" else "bin") / "python"
        if not python_exe.exists():
            self.logger.error("virtual environment not found at %s", venv_path)
            return False
        if not requirements_file.is_file():
            self.logger.warning("requirements file not found: %s", requirements_file)
            return True

        if self.progress_callback:
            self.progress_callback("Installing dependencies...")

        process = await asyncio.create_subprocess_exec(
            str(python_exe),
            "-m",
            "pip",
            "install",
            "-r",
            str(requirements_file),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            self.logger.error("dependency installation failed: %s", stderr.decode())
            return False

        if stdout:
            self.logger.debug(stdout.decode())
        self.logger.info("Dependencies installed from %s", requirements_file)
        return True

    def _validate_python_venv(self) -> bool:
        """Check whether the ``venv`` module is available."""
        try:
            import venv  # noqa: F401

            return True
        except ImportError:
            return False
