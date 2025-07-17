#!/bin/bash
# this_file: scripts/build.sh

set -e

echo "🔧 Building pyxplod..."

# Ensure we're in the project root
cd "$(dirname "$0")/.."

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ src/pyxplod.egg-info/

# Install/update build dependencies
echo "📦 Installing build dependencies..."
uv pip install -e .[dev,test]

# Lint and format code
echo "🎨 Linting and formatting code..."
uv run ruff check --fix src/ tests/
uv run ruff format src/ tests/

# Type checking
echo "🔍 Type checking..."
uv run mypy src/pyxplod tests/

# Run tests
echo "🧪 Running tests..."
uv run pytest tests/ -v --cov=src/pyxplod --cov-report=term-missing

# Build the package
echo "📦 Building package..."
uv run python -m build

echo "✅ Build completed successfully!"
echo "📋 Build artifacts available in dist/"
ls -la dist/