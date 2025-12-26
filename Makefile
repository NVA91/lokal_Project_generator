.PHONY: help install test lint format clean

# Standard targets
help:
	@echo "Verfügbare Befehle:"
	@echo "  make install     - Poetry install + dependencies"
	@echo "  make test        - Alle Tests ausführen"
	@echo "  make lint        - Code linting (flake8 + mypy)"
	@echo "  make format      - Code formatting mit Black"
	@echo "  make clean       - Cache und temporäre Dateien löschen"

install:
	@echo "📦 Installing dependencies with Poetry..."
	poetry install
	@echo "✅ Dependencies installed!"

test:
	@echo "🧪 Running tests with pytest..."
	poetry run pytest tests/ -v --cov=src
	@echo "✅ Tests completed!"

lint:
	@echo "🔍 Linting with flake8..."
	poetry run flake8 src/ tests/
	@echo "🔍 Type checking with mypy..."
	poetry run mypy src/
	@echo "✅ Linting completed!"

format:
	@echo "💄 Formatting code with Black..."
	poetry run black src/ tests/
	@echo "✅ Code formatted!"

clean:
	@echo "🗑️  Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov dist build *.egg-info
	@echo "✅ Cleanup completed!"
