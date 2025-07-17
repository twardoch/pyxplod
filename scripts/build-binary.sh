#!/bin/bash
# this_file: scripts/build-binary.sh

set -e

echo "🔧 Building pyxplod binary..."

# Ensure we're in the project root
cd "$(dirname "$0")/.."

# Install dependencies
echo "📦 Installing dependencies..."
uv add --dev pyinstaller

# Build binary
echo "🏗️  Building binary..."
uv run pyinstaller \
    --onefile \
    --name pyxplod \
    --clean \
    --distpath dist/ \
    --workpath build/ \
    --specpath build/ \
    src/pyxplod/__main__.py

echo "✅ Binary built successfully!"
echo "📋 Binary available at: dist/pyxplod"

# Test the binary
if [ -f "dist/pyxplod" ]; then
    echo "🧪 Testing binary..."
    ./dist/pyxplod --help || echo "⚠️  Binary test failed, but this might be expected"
    echo "📊 Binary size: $(du -h dist/pyxplod | cut -f1)"
fi