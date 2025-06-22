"""project_generator package."""

from .container import Container
from .event_bus import EventBus
from .file_service import FileService
from .template_service import TemplateService
from .plugin_manager import PluginManager


def main(argv=None):
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Project structure generator")
    sub = parser.add_subparsers(dest="command")

    create_parser = sub.add_parser("create", help="Create a new project")
    create_parser.add_argument("name", help="Name of the project")

    args = parser.parse_args(argv)

    if args.command == "create":
        container = Container()
        container.register("file_service", FileService)
        container.register("template_service", TemplateService)

        bus = EventBus()
        plugins = PluginManager()
        plugins.load_plugins(bus, container)

        bus.emit("create_project", args.name)
        print(f"Project '{args.name}' created.")
    else:
        print("Hello from project_generator!")
