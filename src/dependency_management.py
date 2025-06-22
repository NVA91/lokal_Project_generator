from __future__ import annotations

from pathlib import Path
from typing import Iterable, List
import time


class VirtualEnvironmentManager:
    """Manage creation of Python virtual environments."""

    def available_versions(self) -> List[str]:
        """Return available Python versions."""
        return ["3.10", "3.11"]

    def default_python_version(self) -> str:
        return self.available_versions()[0]

    def create_environment(
        self, path: Path, python_version: str, dependencies: Iterable[str]
    ) -> Iterable[int]:
        """Simulate creating a venv and installing dependencies.

        Yields progress percentage values from 0 to 100.
        """
        steps = 5
        for i in range(steps):
            time.sleep(0.1)
            yield int((i + 1) / steps * 100)


class DependencyManager:
    """Manage dependency sets for projects."""

    def available_sets(self) -> List[str]:
        return ["core", "gui", "dev"]

    def resolve(self, selected: Iterable[str]) -> List[str]:
        """Return packages for the given dependency sets."""
        mapping = {
            "core": ["requests"],
            "gui": ["tkinterdnd2"],
            "dev": ["pytest"],
        }
        result: List[str] = []
        for name in selected:
            result.extend(mapping.get(name, []))
        return result
