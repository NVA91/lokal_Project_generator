import logging
from pathlib import Path

from src.template_manager import TemplateManager


def test_create_from_template(tmp_path: Path):
    logger = logging.getLogger("test")
    manager = TemplateManager(logger, Path("templates"))
    assert "smart_home" in manager.available_templates()
    target = tmp_path / "project"
    result = manager.create_from_template("smart_home", target)
    assert result
    assert (target / "pyproject.toml").exists()
    assert (target / "src" / "main.py").exists()
