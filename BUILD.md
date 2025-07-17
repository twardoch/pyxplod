# Build and Release Guide

This document describes the build, test, and release process for pyxplod.

## Prerequisites

- Python 3.10+ 
- [uv](https://github.com/astral-sh/uv) package manager
- Git (for version tagging)

## Local Development

### Setup

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv --python 3.11
uv sync
```

### Running Tests

```bash
# Run the full test suite
./scripts/test.sh

# Run specific test categories
uv run pytest tests/test_package.py -v          # Package tests
uv run pytest tests/test_cli.py -v              # CLI tests
uv run pytest tests/test_integration.py -v      # Integration tests
uv run pytest tests/test_benchmark.py -v        # Benchmark tests

# Run with coverage
uv run pytest tests/ --cov=src/pyxplod --cov-report=html
```

### Building

```bash
# Build Python package
./scripts/build.sh

# Build standalone binary
./scripts/build-binary.sh
```

### Code Quality

```bash
# Lint and format
uv run ruff check src/ tests/
uv run ruff format src/ tests/

# Type checking
uv run mypy src/pyxplod tests/
```

## Release Process

### 1. Prepare Release

Ensure your working directory is clean and all tests pass:

```bash
./scripts/test.sh
```

### 2. Create Git Tag

The version is automatically derived from git tags using semantic versioning:

```bash
# Create and push a new tag
git tag v1.2.3
git push origin v1.2.3
```

Version format: `v{major}.{minor}.{patch}[-{prerelease}]`

Examples:
- `v1.0.0` - Release version
- `v1.0.1` - Patch version
- `v1.1.0` - Minor version
- `v2.0.0` - Major version  
- `v1.0.0-alpha.1` - Pre-release version
- `v1.0.0-beta.1` - Beta version
- `v1.0.0-rc.1` - Release candidate

### 3. Build Release

```bash
./scripts/release.sh
```

This will:
- Verify you're on the tagged commit
- Run the full test suite
- Build the Python package
- Prepare artifacts for distribution

### 4. GitHub Actions (Automatic)

When you push a tag, GitHub Actions will automatically:

1. **Run CI pipeline** on multiple platforms (Linux, macOS, Windows) and Python versions (3.10, 3.11, 3.12)
2. **Build Python package** (wheel and sdist)
3. **Build platform-specific binaries** using PyInstaller
4. **Create GitHub release** with:
   - Release notes from CHANGELOG.md
   - Python package artifacts
   - Binary artifacts for Linux, macOS, and Windows
5. **Publish to PyPI** (if configured)

### 5. Manual PyPI Publishing

If not using automated PyPI publishing:

```bash
# Build first
./scripts/build.sh

# Upload to PyPI
uv run twine upload dist/*

# Or upload to TestPyPI first
uv run twine upload --repository testpypi dist/*
```

## Version Management

### Automatic Versioning

The project uses `hatch-vcs` for automatic version management:

- **Development versions**: `1.0.2.dev0+gb5bff8d.d20250717`
- **Tagged versions**: `1.0.2` (matches the git tag)
- **Dirty working directory**: `1.0.2.dev0+gb5bff8d.d20250717.dirty`

### Version Information

```python
import pyxplod
print(pyxplod.__version__)  # e.g., "1.0.2.dev0+gb5bff8d.d20250717"
```

## Binary Distribution

### Local Binary Build

```bash
./scripts/build-binary.sh
```

Creates a standalone executable at `dist/pyxplod`.

### GitHub Actions Binary Build

The release workflow creates binaries for:
- Linux (x86_64): `pyxplod-linux-amd64`
- macOS (x86_64): `pyxplod-macos-amd64`  
- Windows (x86_64): `pyxplod-windows-amd64.exe`

## Configuration

### GitHub Secrets

For automated PyPI publishing, configure these secrets in your GitHub repository:

- `PYPI_API_TOKEN`: PyPI API token with upload permissions

### Environment Variables

The build system recognizes these environment variables:

- `PYXPLOD_VERSION`: Override version detection
- `PYXPLOD_BUILD_NUMBER`: Build number for CI systems

## Troubleshooting

### Build Issues

1. **Version detection fails**: Ensure you're in a git repository with proper tags
2. **Tests fail**: Run `./scripts/test.sh` to see detailed error messages
3. **Binary build fails**: Check that all dependencies are installed with `uv sync`

### CI/CD Issues

1. **GitHub Actions fails**: Check the workflow logs in the Actions tab
2. **PyPI upload fails**: Verify your API token and package name
3. **Binary build fails**: Ensure PyInstaller is compatible with your dependencies

## Testing Strategy

The test suite includes:

1. **Unit tests** (`tests/test_pyxplod.py`) - Core functionality
2. **CLI tests** (`tests/test_cli.py`) - Command-line interface
3. **Integration tests** (`tests/test_integration.py`) - End-to-end workflows
4. **Benchmark tests** (`tests/test_benchmark.py`) - Performance measurement
5. **Package tests** (`tests/test_package.py`) - Package structure and imports

Run specific test categories using pytest markers:

```bash
uv run pytest -m "unit"        # Unit tests only
uv run pytest -m "integration" # Integration tests only
uv run pytest -m "benchmark"   # Benchmark tests only
```