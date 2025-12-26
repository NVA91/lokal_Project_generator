from pathlib import Path
from typing import Union, Dict, Any


class TemplateService:
    """Service for managing template folders."""

    def __init__(self, templates_dir: Path):
        """Initialize with the directory containing all templates."""
        self.templates_dir = Path(templates_dir)
        self.templates_dir.mkdir(parents=True, exist_ok=True)

    def list_templates(self):
        """Return a sorted list of available template names."""
        return sorted(
            p.name for p in self.templates_dir.iterdir() if p.is_dir()
        )

    def get_template_structure(self, template_name: str) -> Dict[str, Any]:
        """Return a nested dict representing the folder structure."""
        root = self.templates_dir / template_name
        if not root.exists():
            return {}
        structure: Dict[str, Any] = {}
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root)
            parts = relative.parts
            node = structure
            for part in parts[:-1]:
                node = node.setdefault(part, {})
            if path.is_dir():
                node.setdefault(parts[-1], {})
            else:
                node[parts[-1]] = None
        return {template_name: structure}

    def import_template(self, src_path: Union[str, Path]):
        """Import a template folder by copying it into the templates dir."""
        src = Path(src_path)
        dest = self.templates_dir / src.name
        if dest.exists():
            raise FileExistsError(f"Template '{src.name}' already exists")
        if src.is_dir():
            import shutil
            shutil.copytree(src, dest)
        else:
            raise ValueError(
                "Only directories can be imported as templates"
            )
        return dest
