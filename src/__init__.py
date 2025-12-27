"""Project package exposing GUI utilities."""

from .template_service import TemplateService
from .template_preview import TemplatePreview
from .gui import ProjectGeneratorGUI, ProjectGeneratorApp
from .dependency_management import DependencyManager, VirtualEnvironmentManager
from .template_base import (
    TemplateBase,
    SmartHomeTemplate,
    AutomationTemplate,
    GameDevTemplate,
)
from .taupunkt_template import (
    TaupunktTemplate,
    TaupunktAdvancedTemplate,
)

__all__ = [
    "TemplateService",
    "TemplatePreview",
    "ProjectGeneratorGUI",
    "ProjectGeneratorApp",
    "VirtualEnvironmentManager",
    "DependencyManager",
    "TemplateBase",
    "SmartHomeTemplate",
    "AutomationTemplate",
    "GameDevTemplate",
    "TaupunktTemplate",
    "TaupunktAdvancedTemplate",
]
