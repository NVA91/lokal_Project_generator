import asyncio
import logging
from pathlib import Path

from src.venv_manager import VirtualEnvironmentManager


def test_create_venv(tmp_path: Path):
    logger = logging.getLogger("test")
    manager = VirtualEnvironmentManager(logger)
    result = asyncio.run(manager.create_venv(tmp_path))
    assert result
    assert (tmp_path / ".venv").exists()
