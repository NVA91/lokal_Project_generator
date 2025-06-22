import asyncio
from logging import getLogger
from pathlib import Path

from src.virtualenv_manager import VirtualEnvironmentManager


def test_create_venv(tmp_path: Path):
    logger = getLogger("test")
    manager = VirtualEnvironmentManager(logger)
    result = asyncio.run(manager.create_venv(tmp_path))
    assert result
    assert (tmp_path / ".venv").is_dir()


def test_install_dependencies_empty(tmp_path: Path):
    logger = getLogger("test")
    manager = VirtualEnvironmentManager(logger)
    asyncio.run(manager.create_venv(tmp_path))
    requirements = tmp_path / "requirements.txt"
    requirements.write_text("")
    result = asyncio.run(manager.install_dependencies(tmp_path, requirements))
    assert result
