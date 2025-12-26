"""Professional CLI interface using click."""

import sys
from pathlib import Path
import shutil
import click
from click.utils import LazyFile
from src.template_service import TemplateService


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """🚀 lokal_Project_Generator - Professional Project Template System.

    Generate new projects from templates, manage template libraries,
    and automate project setup with ease.
    """
    pass


@cli.command()
@click.option(
    '--template',
    '-t',
    required=True,
    help='Template name to use for generation',
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    required=True,
    help='Output directory for the new project',
)
@click.option(
    '--templates-dir',
    type=click.Path(),
    default='templates',
    help='Path to templates directory (default: ./templates)',
)
def generate(template: str, output: str, templates_dir: str):
    """Generate a new project from a template.

    Example:
        lokal generate --template smart_home --output ~/my_project
    """
    try:
        output_path = Path(output)
        template_path = Path(templates_dir) / template

        # Validation
        if not template_path.exists():
            click.echo(
                click.style(
                    f"❌ Template '{template}' not found in {templates_dir}",
                    fg='red',
                ),
                err=True,
            )
            sys.exit(1)

        if output_path.exists():
            click.echo(
                click.style(
                    f"❌ Output directory '{output}' already exists",
                    fg='red',
                ),
                err=True,
            )
            sys.exit(1)

        # Create project
        with click.progressbar(
            length=100,
            label=f"📦 Generating project from '{template}'",
            show_pos=True,
        ) as bar:
            # Copy template
            shutil.copytree(template_path, output_path)
            if bar is not None:
                bar.update(100)

        click.echo(
            click.style(
                f"✅ Project successfully created at: "
                f"{output_path.absolute()}",
                fg='green',
                bold=True,
            )
        )

    except Exception as e:
        click.echo(
            click.style(f"❌ Error: {str(e)}", fg='red'),
            err=True,
        )
        sys.exit(1)


@cli.command()
@click.option(
    '--templates-dir',
    type=click.Path(),
    default='templates',
    help='Path to templates directory (default: ./templates)',
)
def list(templates_dir: str):
    """List all available templates.

    Example:
        lokal list
    """
    try:
        service = TemplateService(Path(templates_dir))
        templates = service.list_templates()

        if not templates:
            click.echo(
                click.style(
                    "⚠️  No templates found. Use 'lokal import' to "
                    "add templates.",
                    fg='yellow',
                )
            )
            return

        click.echo(
            click.style(
                "\n📚 Available Templates:\n",
                fg='cyan',
                bold=True,
            )
        )

        for i, template_name in enumerate(templates, 1):
            template_path = Path(templates_dir) / template_name
            files_count = sum(
                1 for _ in template_path.rglob('*') if _.is_file()
            )
            click.echo(
                f"  {i}. {click.style(template_name, fg='green')} "
                f"({files_count} files)"
            )

        click.echo()

    except Exception as e:
        click.echo(
            click.style(f"❌ Error: {str(e)}", fg='red'),
            err=True,
        )
        sys.exit(1)


@cli.command()
@click.option(
    '--source',
    '-s',
    required=True,
    type=click.Path(exists=True),
    help='Path to template directory to import',
)
@click.option(
    '--templates-dir',
    type=click.Path(),
    default='templates',
    help='Path to templates directory (default: ./templates)',
)
def import_template(source: str, templates_dir: str):
    """Import a new template from a local directory.

    Example:
        lokal import-template --source ~/my_template
    """
    try:
        service = TemplateService(Path(templates_dir))
        source_path = Path(source)

        if not source_path.is_dir():
            click.echo(
                click.style(
                    f"❌ Source '{source}' is not a directory",
                    fg='red',
                ),
                err=True,
            )
            sys.exit(1)

        with click.progressbar(
            length=100,
            label=f"📥 Importing template '{source_path.name}'",
            show_pos=True,
        ) as bar:
            result = service.import_template(source_path)
            if bar is not None:
                bar.update(100)

        click.echo(
            click.style(
                f"✅ Template successfully imported: {result}",
                fg='green',
                bold=True,
            )
        )

    except FileExistsError as e:
        click.echo(
            click.style(f"❌ {str(e)}", fg='red'),
            err=True,
        )
        sys.exit(1)
    except Exception as e:
        click.echo(
            click.style(f"❌ Error: {str(e)}", fg='red'),
            err=True,
        )
        sys.exit(1)


@cli.command()
@click.option(
    '--templates-dir',
    type=click.Path(),
    default='templates',
    help='Path to templates directory (default: ./templates)',
)
@click.option(
    '--template',
    '-t',
    required=True,
    help='Template name to preview',
)
def preview(template: str, templates_dir: str):
    """Preview template structure and contents.

    Example:
        lokal preview --template smart_home
    """
    try:
        service = TemplateService(Path(templates_dir))
        template_path = Path(templates_dir) / template

        if not template_path.exists():
            click.echo(
                click.style(
                    f"❌ Template '{template}' not found",
                    fg='red',
                ),
                err=True,
            )
            sys.exit(1)

        structure = service.get_template_structure(template)

        click.echo(
            click.style(
                f"\n📋 Template Structure: {template}\n",
                fg='cyan',
                bold=True,
            )
        )

        def print_tree(d: dict, indent: int = 0):
            """Recursively print directory tree."""
            for key, value in d.items():
                prefix = "  " * indent + "├─ "
                if isinstance(value, dict):
                    click.echo(
                        click.style(f"{prefix}📁 {key}/", fg='blue')
                    )
                    print_tree(value, indent + 1)
                else:
                    click.echo(f"{prefix}📄 {key}")

        print_tree(structure)
        click.echo()

    except Exception as e:
        click.echo(
            click.style(f"❌ Error: {str(e)}", fg='red'),
            err=True,
        )
        sys.exit(1)


if __name__ == '__main__':
    cli()
