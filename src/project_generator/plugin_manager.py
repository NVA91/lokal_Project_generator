import importlib
import pkgutil


class PluginManager:
    """Discover and load plugins from a package."""

    def __init__(self, package: str = 'project_generator.plugins'):
        self.package = package
        self.plugins = []

    def load_plugins(self, event_bus, container):
        module = importlib.import_module(self.package)
        for _, name, _ in pkgutil.iter_modules(module.__path__):
            plugin = importlib.import_module(f'{self.package}.{name}')
            if hasattr(plugin, 'register'):
                plugin.register(event_bus, container)
            self.plugins.append(plugin)
