import asyncio
import sys
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Callable
from logging import Logger


class VirtualEnvironmentManager:
    """Manage creation of Python virtual environments."""

    def __init__(self, logger: Logger, progress_callback: Optional[Callable[[str], None]] = None) -> None:
        """Create a new manager instance.

        Parameters
        ----------
        logger:
            Used to emit informational and error log messages.
        progress_callback:
            Optional callable invoked with status messages during environment
            creation.
        """
        self.logger = logger
        self.progress_callback = progress_callback

    async def create_venv(self, project_path: Path) -> bool:
        """Create a virtual environment inside ``project_path``/``.venv``.

        If ``project_path`` does not exist it will be created first.
        """
        venv_path = project_path / ".venv"
        try:
            if not self._validate_python_venv():
                raise EnvironmentError("Python venv module not available")

            project_path.mkdir(parents=True, exist_ok=True)

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
            _, stderr = await process.communicate()

            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, stderr.decode())

            self.logger.info("Virtual environment created at %s", venv_path)
            return True

        except Exception as exc:
            self.logger.error("venv creation failed: %s", exc)
            if venv_path.exists():
                shutil.rmtree(venv_path, ignore_errors=True)
            return False

    def _validate_python_venv(self) -> bool:
        """Check if Python's venv module can be imported."""
        try:
            import venv  # noqa: F401
        except ImportError:
            return False
        return True
