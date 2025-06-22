from __future__ import annotations

"""Project templates for project_generator."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict


class TemplateBase(ABC):
    """Base class for project templates."""

    def __init__(self, root: Path) -> None:
        self.root = Path(root)

    @abstractmethod
    def structure(self) -> Dict[str, Dict | None]:
        """Return a dict describing the directory structure."""

    def create(self) -> None:
        """Create the directory structure on disk."""
        self._create_recursive(self.root, self.structure())

    def _create_recursive(self, base: Path, tree: Dict[str, Dict | None]) -> None:
        for name, subtree in tree.items():
            path = base / name
            path.mkdir(parents=True, exist_ok=True)
            if isinstance(subtree, dict):
                self._create_recursive(path, subtree)


class BasicTemplate(TemplateBase):
    """A simple template with src, tests and docs folders."""

    def structure(self) -> Dict[str, Dict | None]:
        return {"src": {}, "tests": {}, "docs": {}}
