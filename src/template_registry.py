"""Registry for built-in template classes.

Manages dynamic template instantiation and discovery.
"""

from typing import Type, Dict, List, Optional
from .template_base import TemplateBase
from .taupunkt_template import (
    TaupunktTemplate,
    TaupunktAdvancedTemplate,
)


class TemplateRegistry:
    """Registry of available templates (both file-based and programmatic)."""

    def __init__(self):
        """Initialize the registry with built-in templates."""
        self._templates: Dict[str, Type[TemplateBase]] = {}
        self._register_builtin_templates()

    def _register_builtin_templates(self) -> None:
        """Register all built-in template classes."""
        # IoT and Embedded Systems
        self.register("taupunkt", TaupunktTemplate)
        self.register("taupunkt_advanced", TaupunktAdvancedTemplate)

        # Can be extended with other templates like:
        # self.register("smart_home", SmartHomeTemplate)
        # self.register("automation", AutomationTemplate)
        # self.register("game_dev", GameDevTemplate)

    def register(self, name: str, template_class: Type[TemplateBase]) -> None:
        """Register a template class.

        Args:
            name: Unique identifier for the template
            template_class: The template class to register
        """
        if not issubclass(template_class, TemplateBase):
            raise TypeError(
                f"{template_class} must inherit from TemplateBase"
            )
        self._templates[name.lower()] = template_class

    def get(self, name: str) -> Optional[TemplateBase]:
        """Get an instance of a registered template.

        Args:
            name: The template identifier

        Returns:
            An instance of the template, or None if not found
        """
        template_class = self._templates.get(name.lower())
        if template_class:
            return template_class()
        return None

    def get_class(self, name: str) -> Optional[Type[TemplateBase]]:
        """Get the class of a registered template without instantiating.

        Args:
            name: The template identifier

        Returns:
            The template class, or None if not found
        """
        return self._templates.get(name.lower())

    def list_available(self) -> List[str]:
        """List all registered template names.

        Returns:
            Sorted list of template identifiers
        """
        return sorted(self._templates.keys())

    def list_with_descriptions(self) -> Dict[str, str]:
        """List templates with their descriptions.

        Returns:
            Dictionary mapping template names to their descriptions
        """
        result = {}
        for name in self.list_available():
            template = self.get(name)
            if template:
                result[name] = template.get_description()
        return result

    def get_template_info(self, name: str) -> Optional[Dict]:
        """Get comprehensive information about a template.

        Args:
            name: The template identifier

        Returns:
            Dictionary containing template metadata and structure
        """
        template = self.get(name)
        if not template:
            return None

        return {
            "id": name,
            "name": template.get_name(),
            "description": template.get_description(),
            "structure": template.get_structure(),
            "metadata": template.get_metadata(),
        }


# Global registry instance
_default_registry = None


def get_default_registry() -> TemplateRegistry:
    """Get or create the default template registry.

    Returns:
        The global TemplateRegistry instance
    """
    global _default_registry
    if _default_registry is None:
        _default_registry = TemplateRegistry()
    return _default_registry


def list_templates() -> List[str]:
    """Convenience function to list all available templates.

    Returns:
        Sorted list of template identifiers
    """
    return get_default_registry().list_available()


def get_template(name: str) -> Optional[TemplateBase]:
    """Convenience function to get a template instance.

    Args:
        name: The template identifier

    Returns:
        A template instance or None if not found
    """
    return get_default_registry().get(name)


def get_template_info(name: str) -> Optional[Dict]:
    """Convenience function to get template information.

    Args:
        name: The template identifier

    Returns:
        Template information dictionary or None if not found
    """
    return get_default_registry().get_template_info(name)
