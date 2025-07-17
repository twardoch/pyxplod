#!/bin/bash
# this_file: scripts/release.sh

set -e

echo "🚀 Preparing pyxplod release..."

# Ensure we're in the project root
cd "$(dirname "$0")/.."

# Parse version from git tags
VERSION=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
if [ -z "$VERSION" ]; then
    echo "❌ No git tags found. Please create a tag first:"
    echo "   git tag v1.0.0"
    echo "   git push origin v1.0.0"
    exit 1
fi

echo "📋 Releasing version: $VERSION"

# Verify we're on the tagged commit
CURRENT_COMMIT=$(git rev-parse HEAD)
TAG_COMMIT=$(git rev-list -n 1 $VERSION)

if [ "$CURRENT_COMMIT" != "$TAG_COMMIT" ]; then
    echo "⚠️  Warning: Current commit ($CURRENT_COMMIT) differs from tag commit ($TAG_COMMIT)"
    echo "   Consider checking out the tag: git checkout $VERSION"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Run full test suite
echo "🧪 Running full test suite..."
./scripts/test.sh

# Build the package
echo "📦 Building package..."
./scripts/build.sh

# Check if we should publish
echo "📤 Build completed. Ready to publish!"
echo "   To publish to PyPI:"
echo "     uv run twine upload dist/*"
echo "   To publish to TestPyPI:"
echo "     uv run twine upload --repository testpypi dist/*"
echo ""
echo "   Don't forget to create a GitHub release with the built artifacts!"

# Show what was built
echo "📋 Built artifacts:"
ls -la dist/