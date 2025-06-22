import asyncio
import logging
from pathlib import Path

from src.virtualenv_manager import VirtualEnvironmentManager


def test_create_venv(tmp_path: Path):
    logger = logging.getLogger("test")
    logger.addHandler(logging.NullHandler())
    manager = VirtualEnvironmentManager(logger)

    result = asyncio.run(manager.create_venv(tmp_path))

    assert result is True
    assert (tmp_path / ".venv").exists()
