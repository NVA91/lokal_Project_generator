"""Utilities to generate a Python project skeleton with dependency management."""
from pathlib import Path

from .environment import VirtualEnvironmentManager
from .vscode_integration import VSCodeIntegration

PYPROJECT_TEMPLATE = """[build-system]
requires = [\"setuptools>=42\", \"wheel\"]
build-backend = \"setuptools.build_meta\"

[project]
name = "{name}"
version = "0.1.0"
requires-python = ">=3.8"
"""

GITIGNORE_CONTENT = ".venv/\n__pycache__/\n*.pyc\n"

REQUIREMENTS_DEV = "pytest\nblack\nflake8\npip-tools\n"


def write_file(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content)


def generate(project_dir: Path) -> None:
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "src").mkdir(exist_ok=True)
    (project_dir / "tests").mkdir(exist_ok=True)
    (project_dir / "docs").mkdir(exist_ok=True)

    pyproject = PYPROJECT_TEMPLATE.format(name=project_dir.name)
    write_file(project_dir / "pyproject.toml", pyproject)
    write_file(project_dir / ".gitignore", GITIGNORE_CONTENT)
    write_file(project_dir / "requirements.txt", "")
    write_file(project_dir / "requirements-dev.txt", REQUIREMENTS_DEV)
    venv = VirtualEnvironmentManager(project_dir)
    venv.create()
    vscode = VSCodeIntegration(project_dir)
    vscode.setup()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create a Python project structure")
    parser.add_argument("path", nargs="?", default=".", help="Target directory")
    args = parser.parse_args()
    generate(Path(args.path).resolve())
    print("Project initialized at", Path(args.path).resolve())

