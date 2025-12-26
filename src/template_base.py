from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class TemplateBase(ABC):
    """Abstract base class for project templates."""

    @abstractmethod
    def get_name(self) -> str:
        """Return the template's display name."""

    @abstractmethod
    def get_description(self) -> str:
        """Return a short description of the template."""

    @abstractmethod
    def get_structure(self) -> Dict[str, Any]:
        """Return a nested mapping describing the folder structure."""

    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """Return additional metadata such as dependencies."""


class SmartHomeTemplate(TemplateBase):
    """Template for WLED/LED controller projects."""

    def get_name(self) -> str:
        return "Smart Home Controller"

    def get_description(self) -> str:
        return "Starter template for WLED based LED controllers."

    def get_structure(self) -> Dict[str, Any]:
        return {
            "src": {"main.py": None, "controller": {}},
            "docs": {"hardware": {"README.md": None}},
            "assets": {},
            "config": {"wled_config.json": None},
            "README.md": None,
        }

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "dependencies": ["wled", "fastled"],
            "config_files": ["config/wled_config.json"],
        }


class AutomationTemplate(TemplateBase):
    """Template for CI/CD and workflow automation projects."""

    def get_name(self) -> str:
        return "CI/CD Automation"

    def get_description(self) -> str:
        return "Setup for automated build and deployment pipelines."

    def get_structure(self) -> Dict[str, Any]:
        return {
            ".github": {
                "workflows": {"ci.yml": None, "cd.yml": None}
            },
            "scripts": {"deploy.sh": None},
            "docs": {"automation": {"README.md": None}},
            "README.md": None,
        }

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "dependencies": ["docker", "github-actions"],
            "config_files": [
                ".github/workflows/ci.yml",
                ".github/workflows/cd.yml",
            ],
        }


class GameDevTemplate(TemplateBase):
    """Template for a Flutter based card game."""

    def get_name(self) -> str:
        return "Flutter Card Game"

    def get_description(self) -> str:
        return "Boilerplate for a Flutter card game project."

    def get_structure(self) -> Dict[str, Any]:
        return {
            "lib": {"main.dart": None},
            "assets": {"images": {}},
            "docs": {"README.md": None},
            "config": {"pubspec.yaml": None},
        }

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "dependencies": ["flutter", "provider"],
            "config_files": ["pubspec.yaml"],
        }
