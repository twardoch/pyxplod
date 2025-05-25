# pyxplod

# README.md

`pyxplod` is a Python tool that deterministically "explodes" a Python project into a set of files.

- It takes an --input folder
- It takes an --output folder
- It finds all Python files in the input folder recursively
- It reads each .py file into an ast
- In the current .py ast, it finds any `class` definition and any `def` function
- In the output folder, in the sub-folder that corresponds to the relative path of the current .py as, it creates a new .py file for each `class` and `def` function, using the name of the original file plus `_` plus the name of the `class` or `def` function, converted to snake_case and deduplicated. 
- In the current .py ast, it replaces the `class` or `def` definition with a relative import of the file we’ve just created. 
- Once it’s done with the current .py file, saves the modified .py into the output folder, in the sub-folder that corresponds to the relative path of the current .py ast. 
- Repeates this for each .py file in the input folder. 

## How to use it

```
pyxplod --input path/to/input/folder --output path/to/output/folder
```



## Features

- Modern Python packaging with PEP 621 compliance
- Type hints and runtime type checking
- Comprehensive test suite and documentation
- CI/CD ready configuration

## Installation

```bash
uv pip install --system pyxplod
```

## Usage

```python
import pyxplod
```

## Development

This project uses [Hatch](https://hatch.pypa.io/) for development workflow management.

### Setup Development Environment

```bash
# Install hatch if you haven't already
uv pip install --system hatch

# Create and activate development environment
hatch shell

# Run tests
hatch run test

# Run tests with coverage
hatch run test-cov

# Run linting
hatch run lint

# Format code
hatch run format
```

## License

MIT License 