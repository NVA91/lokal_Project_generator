import os


class FileService:
    """Handle filesystem operations."""

    def create_dir(self, path: str):
        os.makedirs(path, exist_ok=True)

    def write_file(self, path: str, content: str):
        self.create_dir(os.path.dirname(path) or '.')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
