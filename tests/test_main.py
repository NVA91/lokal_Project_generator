"""Tests for the main module."""

import subprocess
import sys


def test_main_cli_help():
    """Test that main module loads CLI with help."""
    result = subprocess.run(
        [sys.executable, "-m", "src.main", "--help"], capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "lokal_Project_Generator" in result.stdout
    assert "Commands" in result.stdout


def test_main_cli_version():
    """Test that CLI version command works."""
    result = subprocess.run(
        [sys.executable, "-m", "src.main", "--version"], capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "1.0.0" in result.stdout


def test_main_cli_list():
    """Test that CLI list command works."""
    result = subprocess.run(
        [sys.executable, "-m", "src.main", "list"], capture_output=True, text=True
    )
    assert result.returncode == 0
    # Either templates found or "No templates found" message
    assert "Available Templates" in result.stdout or "No templates found" in result.stdout
