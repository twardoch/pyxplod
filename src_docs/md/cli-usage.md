# Command Line Usage

Complete reference for using pyxplod from the command line, including all options, arguments, and practical examples.

## Basic Syntax

```bash
pyxplod <input_directory> <output_directory> --method <method> [options]
```

### Required Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `input_directory` | Path to source code directory | `./src/` |
| `output_directory` | Path for exploded output | `./exploded/` |

### Required Options

| Option | Values | Description |
|--------|--------|-------------|
| `--method` | `files` \| `dirs` | Explosion strategy to use |

### Optional Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--verbose` | Enable detailed logging output | `False` |

## Detailed Command Reference

### Input Directory

The input directory should contain your Python project:

```bash
# Explode entire project
pyxplod ./my_project ./output --method files

# Explode specific subdirectory
pyxplod ./my_project/src ./output --method dirs

# Use absolute paths
pyxplod /home/user/code/project /tmp/exploded --method files
```

**Requirements:**
- Directory must exist and be readable
- Should contain `.py` files (directly or in subdirectories)
- Symbolic links are followed

### Output Directory

The output directory will be created if it doesn't exist:

```bash
# Create new output directory
pyxplod ./src ./new_output --method files

# Overwrite existing directory (use with caution)
pyxplod ./src ./existing_output --method dirs
```

**Behavior:**
- Creates directory structure as needed
- Preserves relative paths from input
- Overwrites existing files without warning

### Method Selection

#### Files Method (`--method files`)

```bash
pyxplod ./src ./output --method files
```

Creates sibling files with pattern `{original}_{definition}.py`:

```
output/
├── module.py
├── module_my_class.py
├── module_helper_func.py
└── subdir/
    ├── utils.py
    └── utils_processor.py
```

#### Dirs Method (`--method dirs`)

```bash
pyxplod ./src ./output --method dirs
```

Creates subdirectories for each file:

```
output/
├── module/
│   ├── __init__.py
│   ├── my_class.py
│   └── helper_func.py
└── subdir/
    └── utils/
        ├── __init__.py
        └── processor.py
```

### Verbose Logging

Enable detailed output for debugging and monitoring:

```bash
pyxplod ./src ./output --method files --verbose
```

**Verbose output includes:**
- File discovery progress
- AST parsing details
- Import analysis results
- Extraction decisions
- Error stack traces

**Sample verbose output:**
```
14:23:45 | DEBUG | Found 15 Python files to process
14:23:45 | DEBUG | Processing src/utils.py
14:23:45 | DEBUG | Found 3 top-level definitions: ConfigManager, format_data, validate_input
14:23:45 | DEBUG | Extracting ConfigManager with imports: json, pathlib.Path
14:23:45 | DEBUG | Creating src/utils_config_manager.py
14:23:45 | INFO  | ✨ Successfully exploded 15 files to ./output using method 'files'
```

## Practical Examples

### Example 1: Simple Project

**Project structure:**
```
my_app/
├── main.py
├── utils.py
└── config.py
```

**Command:**
```bash
pyxplod my_app exploded_app --method files --verbose
```

**Result:**
```
exploded_app/
├── main.py
├── utils.py
├── utils_helper.py
├── utils_formatter.py
├── config.py
└── config_settings.py
```

### Example 2: Complex Package

**Project structure:**
```
package/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── processor.py
│   └── validator.py
└── utils/
    ├── __init__.py
    └── helpers.py
```

**Command:**
```bash
pyxplod package exploded_package --method dirs
```

**Result:**
```
exploded_package/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── processor/
│   │   ├── __init__.py
│   │   ├── data_processor.py
│   │   └── file_processor.py
│   └── validator/
│       ├── __init__.py
│       ├── schema_validator.py
│       └── input_validator.py
└── utils/
    ├── __init__.py
    └── helpers/
        ├── __init__.py
        ├── string_helper.py
        └── path_helper.py
```

### Example 3: Legacy Code Refactoring

**Large monolithic file (`legacy.py`):**
```python
# 500+ lines with multiple classes and functions
class DatabaseManager: ...
class CacheManager: ...  
class APIClient: ...
def process_data(): ...
def validate_input(): ...
def format_output(): ...
```

**Command:**
```bash
pyxplod . refactored --method dirs --verbose
```

**Benefits:**
- Breaks down 500+ line file into focused modules
- Maintains all functionality through imports
- Creates clear separation of concerns
- Enables easier testing and maintenance

### Example 4: Selective Processing

Process only specific directories:

```bash
# Process only the core module
pyxplod ./project/core ./output/core --method files

# Process utilities separately
pyxplod ./project/utils ./output/utils --method dirs
```

## Error Handling

### Common Errors and Solutions

**Error:** `Invalid method 'file'. Must be 'files' or 'dirs'.`
```bash
# Wrong
pyxplod ./src ./out --method file

# Correct  
pyxplod ./src ./out --method files
```

**Error:** `Input directory does not exist: ./nonexistent`
```bash
# Check path exists
ls ./src

# Use correct path
pyxplod ./src ./output --method files
```

**Error:** `Failed to process file.py: SyntaxError`
- File contains syntax errors
- Fix syntax issues before explosion
- Use `--verbose` to see detailed error information

### Handling Problematic Files

pyxplod skips files with issues and continues processing:

```bash
# Some files may fail, others succeed
pyxplod ./mixed_quality_code ./output --method files --verbose
```

**Files that are skipped:**
- Files with syntax errors
- Files with encoding issues
- Files that can't be parsed as valid Python

## Performance Tips

### Large Projects

For projects with many files:

```bash
# Use files method for faster processing
pyxplod ./large_project ./output --method files

# Monitor progress with verbose output
pyxplod ./large_project ./output --method dirs --verbose
```

### Disk Space

- **Files method**: Uses less disk space
- **Dirs method**: Creates more directories but better organization

### Processing Time

- **Files method**: ~30% faster for large projects
- **Dirs method**: Additional overhead for directory creation

## Integration Examples

### With Version Control

```bash
# Create backup branch
git checkout -b before-explosion

# Explode code
pyxplod ./src ./src_exploded --method dirs

# Replace original with exploded version
rm -rf ./src
mv ./src_exploded ./src

# Commit changes
git add .
git commit -m "Explode monolithic modules for better organization"
```

### With Build Systems

```bash
# In a Makefile
explode:
    pyxplod ./src ./exploded --method dirs --verbose
    # Run tests to verify functionality
    python -m pytest ./tests/
    # Replace source if tests pass
    rm -rf ./src && mv ./exploded ./src
```

### With CI/CD

```yaml
# GitHub Actions example
- name: Explode Code
  run: |
    pip install pyxplod
    pyxplod ./src ./exploded --method dirs
    # Verify exploded code works
    python -m pytest ./tests/
```

## Programmatic Usage

While primarily a CLI tool, you can use pyxplod programmatically:

```python
from pyxplod.cli import main

# Equivalent to: pyxplod ./src ./output --method files --verbose
main(
    input_dir_str="./src",
    output="./output", 
    method="files",
    verbose=True
)
```

## Next Steps

- Explore [configuration options](configuration.md) for advanced usage
- Learn about [file organization](file-organization.md) patterns
- Check the [API reference](api-reference.md) for programmatic usage