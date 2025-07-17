#!/bin/bash
# this_file: scripts/test.sh

set -e

echo "🧪 Running pyxplod test suite..."

# Ensure we're in the project root
cd "$(dirname "$0")/.."

# Install test dependencies
echo "📦 Installing test dependencies..."
uv pip install -e .[dev,test]

# Run linting first
echo "🎨 Running linting..."
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/

# Type checking
echo "🔍 Running type checking..."
uv run mypy src/pyxplod tests/

# Run tests with coverage
echo "🧪 Running tests with coverage..."
uv run pytest tests/ -v \
    --cov=src/pyxplod \
    --cov-report=term-missing \
    --cov-report=html:htmlcov \
    --cov-report=xml:coverage.xml \
    --junit-xml=pytest.xml

# Run benchmarks if available
if [ -f "tests/test_benchmark.py" ]; then
    echo "⚡ Running benchmarks..."
    uv run pytest tests/test_benchmark.py --benchmark-only -v
fi

echo "✅ All tests passed!"

# Show coverage summary
if [ -f "htmlcov/index.html" ]; then
    echo "📊 Coverage report available at: htmlcov/index.html"
fi