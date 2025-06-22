"""Main entry point for the project_generator package."""

from argparse import ArgumentParser
from pathlib import Path

from .templates import BasicTemplate


def main(args: list[str] | None = None) -> None:
    """Generate a simple project structure and greet the user."""
    parser = ArgumentParser(description="Create a basic project structure")
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Target directory where the structure should be created",
    )
    parsed = parser.parse_args(args)

    template = BasicTemplate(Path(parsed.path))
    template.create()

    print("Hello from project_generator!")


if __name__ == "__main__":
    main()
