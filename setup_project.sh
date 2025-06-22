#!/bin/sh
# Create basic folder structure
mkdir -p src tests docs

# Initialize virtual environment
if [ ! -d ".venv" ]; then
  python -m venv .venv
  echo "Virtual environment created. Activate with: source .venv/bin/activate"
fi

echo "Install development dependencies with: pip install .[dev]"

echo "Project structure ready."
