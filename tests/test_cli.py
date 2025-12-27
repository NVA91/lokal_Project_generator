"""Tests for the CLI module."""

import pytest
from pathlib import Path
from click.testing import CliRunner
from src.cli import cli
import shutil
import tempfile


@pytest.fixture
def runner():
    """Create a CLI test runner."""
    return CliRunner()


@pytest.fixture
def temp_templates():
    """Create a temporary templates directory with sample template."""
    temp_dir = Path(tempfile.mkdtemp())
    templates_dir = temp_dir / "templates"
    templates_dir.mkdir()

    # Create a sample template
    sample_template = templates_dir / "sample"
    sample_template.mkdir()
    (sample_template / "README.md").write_text("# Sample Project")
    (sample_template / "config.json").write_text('{"name": "sample"}')

    yield temp_dir, templates_dir

    # Cleanup
    shutil.rmtree(temp_dir)


def test_cli_version(runner):
    """Test CLI version command."""
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "1.0.0" in result.output


def test_cli_help(runner):
    """Test CLI help command."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "lokal_Project_Generator" in result.output


def test_generate_command_success(runner, temp_templates):
    """Test successful project generation."""
    temp_dir, templates_dir = temp_templates
    output_dir = temp_dir / "new_project"

    result = runner.invoke(
        cli,
        [
            "generate",
            "--template",
            "sample",
            "--output",
            str(output_dir),
            "--templates-dir",
            str(templates_dir),
        ],
    )

    assert result.exit_code == 0
    assert "successfully created" in result.output.lower()
    assert output_dir.exists()
    assert (output_dir / "README.md").exists()
    assert (output_dir / "config.json").exists()


def test_generate_command_missing_template(runner, temp_templates):
    """Test generate with non-existent template."""
    temp_dir, templates_dir = temp_templates
    output_dir = temp_dir / "new_project"

    result = runner.invoke(
        cli,
        [
            "generate",
            "--template",
            "nonexistent",
            "--output",
            str(output_dir),
            "--templates-dir",
            str(templates_dir),
        ],
    )

    assert result.exit_code != 0
    assert "not found" in result.output.lower()


def test_generate_command_existing_output(runner, temp_templates):
    """Test generate with existing output directory."""
    temp_dir, templates_dir = temp_templates
    output_dir = temp_dir / "existing"
    output_dir.mkdir()

    result = runner.invoke(
        cli,
        [
            "generate",
            "--template",
            "sample",
            "--output",
            str(output_dir),
            "--templates-dir",
            str(templates_dir),
        ],
    )

    assert result.exit_code != 0
    assert "already exists" in result.output.lower()


def test_list_command_with_templates(runner, temp_templates):
    """Test listing available templates."""
    temp_dir, templates_dir = temp_templates

    result = runner.invoke(cli, ["list", "--templates-dir", str(templates_dir)])

    assert result.exit_code == 0
    assert "Available Templates" in result.output
    assert "sample" in result.output


def test_list_command_empty(runner, temp_templates):
    """Test listing templates when none exist."""
    temp_dir, templates_dir = temp_templates
    empty_dir = temp_dir / "empty_templates"
    empty_dir.mkdir()

    result = runner.invoke(cli, ["list", "--templates-dir", str(empty_dir)])

    assert result.exit_code == 0
    assert "No templates found" in result.output


def test_import_template_command_success(runner, temp_templates):
    """Test importing a template."""
    temp_dir, templates_dir = temp_templates

    # Create a template to import
    import_src = temp_dir / "import_src"
    import_src.mkdir()
    (import_src / "main.py").write_text("print('hello')")
    (import_src / "setup.py").write_text("# setup")

    result = runner.invoke(
        cli, ["import-template", "--source", str(import_src), "--templates-dir", str(templates_dir)]
    )

    assert result.exit_code == 0
    assert "successfully imported" in result.output.lower()
    assert (templates_dir / "import_src").exists()


def test_import_template_duplicate(runner, temp_templates):
    """Test importing template with duplicate name."""
    temp_dir, templates_dir = temp_templates

    # Try to import with same name as existing
    import_src = temp_dir / "sample"
    import_src.mkdir()

    result = runner.invoke(
        cli, ["import-template", "--source", str(import_src), "--templates-dir", str(templates_dir)]
    )

    assert result.exit_code != 0
    assert "already exists" in result.output.lower()


def test_preview_command_success(runner, temp_templates):
    """Test preview command."""
    temp_dir, templates_dir = temp_templates

    result = runner.invoke(
        cli, ["preview", "--template", "sample", "--templates-dir", str(templates_dir)]
    )

    assert result.exit_code == 0
    assert "Template Structure" in result.output
    assert "sample" in result.output


def test_preview_nonexistent_template(runner, temp_templates):
    """Test preview with non-existent template."""
    temp_dir, templates_dir = temp_templates

    result = runner.invoke(
        cli, ["preview", "--template", "nonexistent", "--templates-dir", str(templates_dir)]
    )

    assert result.exit_code != 0
    assert "not found" in result.output.lower()
