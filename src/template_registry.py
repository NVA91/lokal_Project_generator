from typing import Type, Dict, List, Optional, Any
from src.template_base import TemplateBase
from src.taupunkt_template import TaupunktTemplate, TaupunktAdvancedTemplate
from src.esp32_templates import SHT41TemperatureHumidityTemplate


class TemplateRegistry:
    def __init__(self) -> None:  # Typ-Anmerkung fix
        self._templates: Dict[str, Type[TemplateBase]] = {}
        self._register_builtin_templates()

    def _register_builtin_templates(self) -> None:
        self.register("taupunkt", TaupunktTemplate)
        self.register("taupunkt_advanced", TaupunktAdvancedTemplate)
        self.register("esp32_sht41", SHT41TemperatureHumidityTemplate)

    def register(self, name: str, template_class: Type[TemplateBase]) -> None:
        self._templates[name.lower()] = template_class

    def list_available(self) -> List[str]:
        return sorted(self._templates.keys())

    def get_template_info(self, name: str) -> Optional[Dict[str, Any]]:
        template_class = self._templates.get(name.lower())
        if not template_class:
            return None
        template = template_class()
        return {
            "id": name,
            "name": template.get_name(),
            "structure": template.get_structure(),
            "metadata": template.get_metadata(),
        }


_default_registry = None


def get_default_registry() -> TemplateRegistry:
    global _default_registry
    if _default_registry is None:
        _default_registry = TemplateRegistry()
    return _default_registry


def get_template(name: str) -> Optional[TemplateBase]:
    template_class = get_default_registry()._templates.get(name.lower())
    return template_class() if template_class else None
