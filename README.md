# project_generator

A small helper to demonstrate a modern Python project structure.

## Structure

- `src/project_generator/`: package source code
- `tests/`: unit tests
- `docs/`: documentation

## Usage

Run without arguments to see a greeting:

```bash
python -m project_generator
```

Create a new project skeleton:

```bash
python -m project_generator create my_project
```

This will create directories like `my_project/src` and `my_project/tests` and
populate files such as `.gitignore`, `pyproject.toml` and a basic GitHub
Actions workflow for linting and tests.

## Development Setup

Create the folder structure and a virtual environment:

```bash
./setup_project.sh
```

Install dependencies (requires `pip`):

```bash
pip install -r requirements.txt
```

Run tests:

```bash
./run_tests.sh
```
