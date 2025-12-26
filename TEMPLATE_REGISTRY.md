# Template Registry System

The project generator now supports a dynamic template registry system that enables easy registration and discovery of project templates.

## Overview

The template registry provides:

- **Dynamic Registration** - Register template classes at runtime
- **Template Discovery** - List all available templates with descriptions
- **Programmatic Access** - Instantiate templates from code
- **Metadata Inspection** - Examine template structure and configuration before generation

## Architecture

### TemplateRegistry

The `TemplateRegistry` class manages all available templates:

```python
from src.template_registry import TemplateRegistry, get_default_registry

# Get the global registry
registry = get_default_registry()

# List all templates
for template_name in registry.list_available():
    print(template_name)

# Get a template instance
template = registry.get("taupunkt")

# Get template metadata
info = registry.get_template_info("taupunkt")
print(info['structure'])  # Folder structure
print(info['metadata'])   # Hardware config, dependencies, etc.
```

### Template Classes

All templates inherit from `TemplateBase` and must implement:

```python
class MyTemplate(TemplateBase):
    def get_name(self) -> str:
        """Display name of the template."""
        return "My Template"
    
    def get_description(self) -> str:
        """Short description of what this template does."""
        return "A template for..."
    
    def get_structure(self) -> Dict[str, Any]:
        """Nested dict representing folder structure."""
        return {
            "src": {
                "main.py": None,
                "utils": {"helper.py": None}
            },
            "tests": {"test_main.py": None},
            "README.md": None
        }
    
    def get_metadata(self) -> Dict[str, Any]:
        """Configuration, dependencies, hardware specs, etc."""
        return {
            "framework": "Python 3.9",
            "dependencies": ["requests", "pydantic"],
            "features": ["Feature 1", "Feature 2"],
        }
```

## Built-in Templates

### Taupunkt

**ID**: `taupunkt`

**Description**: MicroPython-based environmental monitoring and dew point display for Raspberry Pi Pico 2.

**Features**:
- Real-time dew point calculation
- Multi-sensor support (AHT20, BMP280, SHT41)
- ST7789 LCD display
- Calibration support
- Local data logging

**Hardware**:
- Controller: Raspberry Pi Pico 2
- Display: Waveshare 1.47" ST7789
- Sensors: AHT20, BMP280, SHT41

**See**: [Taupunkt Documentation](./docs/TAUPUNKT_TEMPLATE.md)

### Taupunkt Advanced

**ID**: `taupunkt_advanced`

**Description**: Extended Taupunkt with cloud connectivity, web interface, and analytics.

**Additional Features**:
- MQTT connectivity
- RESTful API
- Web dashboard
- Cloud data sync
- Real-time notifications

**See**: [Taupunkt Documentation](./docs/TAUPUNKT_TEMPLATE.md)

## Usage Examples

### List Available Templates

```python
from src.template_registry import list_templates

for name in list_templates():
    print(f"  - {name}")
```

### Get Template Information

```python
from src.template_registry import get_template_info

info = get_template_info("taupunkt")

print(f"Name: {info['name']}")
print(f"Description: {info['description']}")
print(f"Dependencies: {info['metadata']['dependencies']}")
```

### Create Template Instance

```python
from src.template_registry import get_template

template = get_template("taupunkt")
if template:
    structure = template.get_structure()
    metadata = template.get_metadata()
    print(f"Creating {template.get_name()} project...")
```

### Generate Project from Template

```python
from src.template_registry import get_template
from pathlib import Path

template = get_template("taupunkt")
if template:
    # Get structure
    structure = template.get_structure()
    
    # Create project directory
    project_root = Path("./my_taupunkt_project")
    project_root.mkdir(exist_ok=True)
    
    # Create folders and files
    def create_structure(base, struct):
        for name, content in struct.items():
            path = base / name
            if isinstance(content, dict):
                path.mkdir(exist_ok=True)
                create_structure(path, content)
            else:  # It's a file
                path.touch()
    
    create_structure(project_root, structure)
    print(f"Project created at {project_root}")
```

### GUI Integration

The template registry can be integrated into the GUI to show available templates:

```python
from src.template_registry import list_templates, get_template_info
from PyQt6.QtWidgets import QComboBox

# Populate combo box with templates
combo = QComboBox()
for template_name in list_templates():
    info = get_template_info(template_name)
    combo.addItem(info['name'], template_name)

# When selection changes, show description and structure
def on_template_selected(index):
    template_id = combo.currentData()
    info = get_template_info(template_id)
    description_label.setText(info['description'])
    # Show structure in tree widget, metadata in table, etc.
```

## Adding New Templates

### 1. Create Template Class

Create a new file (e.g., `src/my_template.py`):

```python
from .template_base import TemplateBase
from typing import Dict, Any

class MyTemplate(TemplateBase):
    def get_name(self) -> str:
        return "My Awesome Template"
    
    def get_description(self) -> str:
        return "A template for building amazing things"
    
    def get_structure(self) -> Dict[str, Any]:
        return {
            "src": {"main.py": None},
            "tests": {"test_main.py": None},
            "README.md": None,
        }
    
    def get_metadata(self) -> Dict[str, Any]:
        return {
            "framework": "Python 3.9+",
            "dependencies": ["requests"],
            "features": ["Feature 1", "Feature 2"],
        }
```

### 2. Register Template

Update `src/template_registry.py`:

```python
from .my_template import MyTemplate

class TemplateRegistry:
    def _register_builtin_templates(self) -> None:
        # ... existing templates ...
        self.register("my_template", MyTemplate)
```

### 3. Update Package Exports

Update `src/__init__.py`:

```python
from .my_template import MyTemplate

__all__ = [
    # ... existing exports ...
    'MyTemplate',
]
```

### 4. Add Documentation

Create `docs/MY_TEMPLATE.md` with:
- Overview and features
- Hardware/software requirements
- Project structure explanation
- Usage examples
- Configuration options
- Troubleshooting guide

### 5. Create Example

Create `examples/my_template_example.py` demonstrating:
- Template discovery
- Structure inspection
- Metadata reading
- Project generation

## Best Practices

### Template Design

1. **Clear Structure** - Folder organization should match the intended workflow
2. **Complete Metadata** - Provide comprehensive configuration and hardware specs
3. **Documentation** - Include thorough guides for users
4. **Examples** - Provide working code samples
5. **Defaults** - Include sensible configuration defaults

### Naming Conventions

- **Template IDs**: lowercase with underscores (e.g., `my_template`)
- **Display Names**: Title case, descriptive (e.g., "My Awesome Template")
- **File Names**: Follow project conventions (snake_case for Python)

### Configuration Files

- Use JSON for static configuration
- Include example/default config files in template
- Document all configuration options in metadata

## Running Examples

```bash
# Run Taupunkt template examples
python examples/taupunkt_example.py

# Output:
# == Available Templates ==
#   Taupunkt - Dew Point Display
#     ID: taupunkt
#     ...
```

## Future Enhancements

- Template versioning
- Dependency resolution
- Template inheritance/composition
- Configuration wizard integration
- Automated validation and testing
- Template marketplace/repository

## Troubleshooting

### Template not found

```python
from src.template_registry import get_default_registry

registry = get_default_registry()
if "mytemplate" not in registry.list_available():
    print("Template not registered")
```

### Import errors

Ensure template class is properly imported in `template_registry.py`.

### Metadata issues

Verify `get_metadata()` returns a valid dictionary with all required keys.

## API Reference

### TemplateRegistry

```python
class TemplateRegistry:
    def register(name: str, template_class: Type[TemplateBase]) -> None
    def get(name: str) -> Optional[TemplateBase]
    def get_class(name: str) -> Optional[Type[TemplateBase]]
    def list_available() -> List[str]
    def list_with_descriptions() -> Dict[str, str]
    def get_template_info(name: str) -> Optional[Dict]
```

### Convenience Functions

```python
# Get global registry
get_default_registry() -> TemplateRegistry

# List templates
list_templates() -> List[str]

# Get template instance
get_template(name: str) -> Optional[TemplateBase]

# Get template info
get_template_info(name: str) -> Optional[Dict]
```

## License

See LICENSE file in project root.
