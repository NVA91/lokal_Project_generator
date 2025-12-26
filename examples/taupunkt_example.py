#!/usr/bin/env python3
"""Example: Using the Taupunkt template.

Demonstrates how to:
1. Access the Taupunkt template from the registry
2. Inspect its structure and metadata
3. Generate a project with specific configuration
"""

from src.template_registry import (
    get_template_info,
    get_template,
    list_templates,
)
import json
from pathlib import Path


def example_list_templates():
    """List all available templates."""
    print("\n=== Available Templates ===")
    templates = list_templates()
    for template_name in templates:
        info = get_template_info(template_name)
        if info:
            print(f"\n  {info['name']}")
            print(f"    ID: {info['id']}")
            print(f"    Description: {info['description']}")


def example_taupunkt_structure():
    """Inspect the Taupunkt template structure."""
    print("\n=== Taupunkt Template Structure ===")
    info = get_template_info("taupunkt")
    if info:
        print(f"\nTemplate: {info['name']}")
        print(f"Description: {info['description']}\n")
        print("Folder Structure:")
        _print_tree(info['structure'], indent=0)


def example_taupunkt_metadata():
    """Show Taupunkt template metadata."""
    print("\n=== Taupunkt Metadata ===")
    info = get_template_info("taupunkt")
    if info:
        metadata = info['metadata']
        print(f"\nFramework: {metadata.get('framework')}")
        print(f"Platform: {metadata.get('platform')}")
        print(f"Language: {metadata.get('language')}")
        
        print(f"\nDependencies:")
        for dep in metadata.get('dependencies', []):
            print(f"  - {dep}")
        
        print(f"\nHardware Configuration:")
        controller = metadata.get('controller_specs', {})
        print(f"  Controller: {controller.get('model')}")
        print(f"  Processor: {controller.get('processor')}")
        print(f"  Frequency: {controller.get('frequency')}")
        print(f"  RAM: {controller.get('ram')}")
        print(f"  Flash: {controller.get('flash')}")
        
        print(f"\nSensors:")
        for sensor in metadata.get('dew_point_sensors', []):
            print(f"  - {sensor['name']} @ 0x{sensor['address']}")
            print(f"    Type: {sensor['type']}")
        
        print(f"\nFeatures:")
        for feature in metadata.get('features', []):
            print(f"  ✓ {feature}")


def example_taupunkt_advanced_metadata():
    """Show advanced Taupunkt template metadata."""
    print("\n=== Taupunkt Advanced Metadata ===")
    info = get_template_info("taupunkt_advanced")
    if info:
        metadata = info['metadata']
        print(f"\nTemplate: {info['name']}")
        print(f"Description: {info['description']}")
        
        if 'advanced_features' in metadata:
            print(f"\nAdvanced Features:")
            for category, features in metadata['advanced_features'].items():
                print(f"  {category.title()}:")
                for feature in features:
                    print(f"    - {feature}")


def example_create_project():
    """Example of creating a Taupunkt project."""
    print("\n=== Creating a Taupunkt Project ===")
    
    template = get_template("taupunkt")
    if not template:
        print("Taupunkt template not found!")
        return
    
    # Get the structure
    structure = template.get_structure()
    
    # Create a sample project directory
    project_dir = Path("./taupunkt_project_sample")
    
    print(f"\nProject structure would be created at: {project_dir}")
    print(f"Total folders: {_count_dirs(structure)}")
    print(f"Total files: {_count_files(structure)}")
    
    # Show configuration files
    metadata = template.get_metadata()
    if 'config_files' in metadata:
        print(f"\nConfiguration files:")
        for config_file in metadata['config_files']:
            print(f"  - {config_file}")
    
    print(f"\nPin Configuration:")
    pins = metadata.get('pin_configuration', {})
    for pin_name, pin_value in pins.items():
        print(f"  {pin_name}: {pin_value}")


def _print_tree(structure: dict, indent: int = 0):
    """Pretty-print a structure dict as a tree."""
    prefix = "  " * indent
    for name, content in sorted(structure.items()):
        if isinstance(content, dict) and content:
            print(f"{prefix}├─ {name}/")
            _print_tree(content, indent + 1)
        else:
            print(f"{prefix}├─ {name}")


def _count_dirs(structure: dict) -> int:
    """Recursively count directories in structure."""
    count = 0
    for name, content in structure.items():
        if isinstance(content, dict):
            count += 1
            count += _count_dirs(content)
    return count


def _count_files(structure: dict) -> int:
    """Recursively count files in structure."""
    count = 0
    for name, content in structure.items():
        if content is None:  # It's a file
            count += 1
        elif isinstance(content, dict):
            count += _count_files(content)
    return count


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Taupunkt Template Examples")
    print("=" * 60)
    
    example_list_templates()
    example_taupunkt_structure()
    example_taupunkt_metadata()
    example_taupunkt_advanced_metadata()
    example_create_project()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60 + "\n")
