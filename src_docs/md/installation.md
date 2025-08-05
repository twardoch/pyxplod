# Installation & Setup

This guide covers everything you need to install and set up pyxplod on your system.

## Requirements

- **Python 3.9+** (pyxplod uses modern Python features)
- **uv** (recommended) or pip for package management
- Command-line access

## Installation Methods

### Method 1: Install from PyPI (Recommended)

```bash
uv pip install pyxplod
```

Or with traditional pip:
```bash
pip install pyxplod
```

### Method 2: Install from Source

1. Clone the repository:
```bash
git clone https://github.com/twardoch/pyxplod.git
cd pyxplod
```

2. Install using uv:
```bash
uv pip install .
```

Or for development:
```bash
uv pip install -e .
```

### Method 3: Development Setup

For contributors and developers:

```bash
git clone https://github.com/twardoch/pyxplod.git
cd pyxplod
uv venv --python 3.12
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

## Verification

Verify your installation by running:

```bash
pyxplod --help
```

You should see the help message with available commands and options.

## Dependencies

pyxplod has minimal dependencies:

- **fire**: For command-line interface parsing
- **loguru**: For enhanced logging capabilities  
- **rich**: For beautiful terminal output

These are automatically installed when you install pyxplod.

## Platform Support

pyxplod is cross-platform and works on:

- **Linux** (tested on Ubuntu, Debian, RHEL)
- **macOS** (tested on 10.15+)
- **Windows** (tested on Windows 10/11)

## Troubleshooting

### Common Issues

**Issue**: `pyxplod: command not found`
- **Solution**: Ensure your Python scripts directory is in your PATH, or use `python -m pyxplod`

**Issue**: Permission denied errors
- **Solution**: Use `--user` flag with pip: `pip install --user pyxplod`

**Issue**: Module import errors
- **Solution**: Ensure you're using the correct Python environment where pyxplod is installed

### Getting Help

If you encounter issues:

1. Check the [troubleshooting section](configuration.md#troubleshooting) in configuration
2. Review existing [GitHub issues](https://github.com/twardoch/pyxplod/issues)
3. Create a new issue with:
   - Your Python version (`python --version`)
   - Your operating system
   - Complete error message
   - Minimal code example that reproduces the issue

## Next Steps

Once installed, proceed to the [Quick Start Guide](quickstart.md) to begin using pyxplod!