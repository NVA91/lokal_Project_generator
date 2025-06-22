import os


def register(event_bus, container):
    def create_handler(path: str):
        fs = container.get("file_service")
        ts = container.get("template_service")
        name = os.path.basename(path)

        # basic package layout
        package_dir = os.path.join(path, "src", name)
        fs.create_dir(package_dir)
        fs.create_dir(os.path.join(path, "tests"))
        fs.write_file(os.path.join(package_dir, "__init__.py"), "")

        # README
        readme_content = ts.render("# {project}\n", {"project": name})
        fs.write_file(os.path.join(path, "README.md"), readme_content)

        # .gitignore
        gitignore = "\n".join([
            "__pycache__/",
            ".pytest_cache/",
            "venv/",
        ])
        fs.write_file(os.path.join(path, ".gitignore"), gitignore)

        # pyproject.toml
        pyproject = "\n".join(
            [
                "[build-system]",
                "requires = ['setuptools>=42', 'wheel']",
                "build-backend = 'setuptools.build_meta'",
                "",
                "[project]",
                f"name = '{name}'",
                "version = '0.1.0'",
                "requires-python = '>=3.8'",
                "dependencies = ['requests']",
                "",
                "[project.optional-dependencies]",
                "dev = ['black', 'flake8', 'pytest']",
            ]
        )
        fs.write_file(os.path.join(path, "pyproject.toml"), pyproject)

        # GitHub Actions workflow
        workflow = "\n".join(
            [
                "name: CI",
                "on: [push, pull_request]",
                "jobs:",
                "  build:",
                "    runs-on: ubuntu-latest",
                "    steps:",
                "      - uses: actions/checkout@v3",
                "      - uses: actions/setup-python@v4",
                "        with:",
                "          python-version: '3.x'",
                "      - run: pip install black flake8 pytest",
                "      - run: flake8 src tests",
                "      - run: black --check src tests",
                "      - run: pytest -q",
            ]
        )
        fs.write_file(
            os.path.join(path, ".github", "workflows", "ci.yml"), workflow
        )

    event_bus.subscribe('create_project', create_handler)
