"""Manage project templates."""

from __future__ import annotations

import shutil
from pathlib import Path
from logging import Logger


class TemplateManager:
    """Handles creation of project folders from templates."""

    def __init__(self, logger: Logger, templates_dir: Path | None = None):
        self.logger = logger
        self.templates_dir = templates_dir or Path(__file__).resolve().parent.parent / "templates"

    def available_templates(self) -> list[str]:
        """Return a list of available template names."""
        if not self.templates_dir.exists():
            return []
        return [d.name for d in self.templates_dir.iterdir() if d.is_dir()]

    def create_from_template(self, template_name: str, target_path: Path) -> bool:
        """Copy a template into the target path."""
        source = self.templates_dir / template_name
        if not source.is_dir():
            self.logger.error("Template '%s' does not exist", template_name)
            return False
        try:
            shutil.copytree(source, target_path)
            self.logger.info("Project created at %s", target_path)
            return True
        except Exception as exc:  # noqa: BLE001
            self.logger.error("Failed to create project: %s", exc)
            return False
