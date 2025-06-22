import subprocess
import sys
import os
import shutil


def run_module(args):
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.abspath("src")
    return subprocess.run([sys.executable, "-m", "project_generator", *args], capture_output=True, text=True, env=env)


def test_main_output():
    result = run_module([])
    assert result.returncode == 0
    assert "Hello from project_generator" in result.stdout


def test_create_command(tmp_path):
    project = tmp_path / "sample"
    result = run_module(["create", str(project)])
    assert result.returncode == 0
    assert project.joinpath("README.md").exists()
    pkg_dir = project.joinpath("src", "sample")
    assert pkg_dir.is_dir()
    assert pkg_dir.joinpath("__init__.py").exists()
    assert project.joinpath("tests").is_dir()
    assert project.joinpath(".gitignore").exists()
    pyproject = project.joinpath("pyproject.toml")
    assert pyproject.exists()
    content = pyproject.read_text()
    assert "dependencies" in content
    assert project.joinpath(".github", "workflows", "ci.yml").exists()
