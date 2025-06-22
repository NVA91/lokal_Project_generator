#!/bin/sh
# Create basic folder structure
mkdir -p src tests docs

# Create default pyproject.toml if missing
if [ ! -f pyproject.toml ]; then
cat <<EOT > pyproject.toml
[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "$(basename "$PWD")"
version = "0.1.0"
requires-python = ">=3.8"
EOT
fi

# Ensure dependency files exist
touch requirements.txt requirements-dev.txt

# Initialize virtual environment
if [ ! -d ".venv" ]; then
  python -m venv .venv
  echo "Virtual environment created. Activate with: source .venv/bin/activate"
fi

echo "Project structure ready."
