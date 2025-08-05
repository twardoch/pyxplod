# Configuration Options

Advanced configuration and customization options for pyxplod, including environment variables, logging settings, and troubleshooting guidance.

## Configuration Overview

pyxplod is designed to work out-of-the-box with sensible defaults, but offers several configuration options for customization:

- **Runtime Configuration**: Command-line flags and options
- **Environment Variables**: System-level settings
- **Logging Configuration**: Output verbosity and formatting
- **Path Handling**: Input/output directory management

## Command-Line Configuration

### Core Options

```bash
pyxplod <input> <output> --method <method> [flags]
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `input` | string | ✅ | Input directory path |
| `output` | string | ✅ | Output directory path |
| `--method` | `files`\|`dirs` | ✅ | Explosion method |
| `--verbose` | flag | ❌ | Enable verbose logging |

### Advanced Usage

#### Path Specifications

```bash
# Relative paths
pyxplod ./src ./output --method files

# Absolute paths  
pyxplod /home/user/project /tmp/exploded --method dirs

# Complex directory structures
pyxplod ./deep/nested/source ./flat/output --method files

# Current directory
pyxplod . ./exploded --method dirs
```

#### Method-Specific Behavior

**Files Method Configuration:**
```bash
# Standard files method
pyxplod ./src ./out --method files

# With verbose output for debugging
pyxplod ./src ./out --method files --verbose
```

**Dirs Method Configuration:**
```bash
# Standard dirs method
pyxplod ./src ./out --method dirs

# Dirs method with detailed logging
pyxplod ./src ./out --method dirs --verbose
```

## Environment Variables

### Logging Configuration

```bash
# Set log level (DEBUG, INFO, WARNING, ERROR)
export PYXPLOD_LOG_LEVEL=DEBUG

# Custom log format
export PYXPLOD_LOG_FORMAT="{time} | {level} | {file} | {message}"

# Log to file instead of console
export PYXPLOD_LOG_FILE="./pyxplod.log"
```

### Path Configuration

```bash
# Default input directory
export PYXPLOD_DEFAULT_INPUT="./src"

# Default output directory  
export PYXPLOD_DEFAULT_OUTPUT="./exploded"

# Default method
export PYXPLOD_DEFAULT_METHOD="files"
```

### Performance Tuning

```bash
# File processing batch size
export PYXPLOD_BATCH_SIZE=10

# Maximum file size to process (in MB)
export PYXPLOD_MAX_FILE_SIZE=50

# Skip files with syntax errors
export PYXPLOD_SKIP_ERRORS=true
```

## Logging Configuration

### Verbosity Levels

#### Standard Output (Default)

```bash
pyxplod ./src ./out --method files
```

**Output:**
```
Found 12 Python files to process
✨ Successfully exploded 12 files to ./out using method 'files'
```

#### Verbose Output

```bash
pyxplod ./src ./out --method files --verbose
```

**Output:**
```
14:23:01 | DEBUG | Starting pyxplod with method: files
14:23:01 | DEBUG | Input path: /home/user/src (resolved)
14:23:01 | DEBUG | Output path: /home/user/out (resolved)
14:23:01 | DEBUG | Scanning for Python files...
14:23:01 | DEBUG | Found Python file: src/module1.py
14:23:01 | DEBUG | Found Python file: src/module2.py
14:23:01 | INFO  | Found 2 Python files to process
14:23:01 | DEBUG | Processing src/module1.py
14:23:01 | DEBUG | Parsing AST for src/module1.py
14:23:01 | DEBUG | Found top-level definitions: ['MyClass', 'helper_function']
14:23:01 | DEBUG | Extracting MyClass with dependencies: ['json', 'pathlib']
14:23:01 | DEBUG | Creating file: out/module1_my_class.py
14:23:01 | DEBUG | Extracting helper_function with dependencies: ['os']
14:23:01 | DEBUG | Creating file: out/module1_helper_function.py
14:23:01 | DEBUG | Updating original file: out/module1.py
14:23:01 | INFO  | ✨ Successfully exploded 2 files to ./out using method 'files'
```

### Custom Logging Setup

For programmatic usage, configure logging directly:

```python
from loguru import logger
from rich.console import Console
from pyxplod.cli import main

# Custom console
console = Console()

# Configure logger
logger.remove()
logger.add(
    console.print, 
    format="{time:HH:mm:ss} | {level} | {message}",
    level="INFO"
)

# Run with custom logging
main("./src", "./output", method="files", verbose=True)
```

## File Handling Configuration

### File Discovery Rules

pyxplod follows these rules when scanning for Python files:

```python
# Files included
INCLUDED_PATTERNS = [
    "*.py",           # All Python files
    "*/__init__.py",  # Package initialization
    "*/__main__.py"   # Module entry points
]

# Directories excluded
EXCLUDED_DIRS = [
    "__pycache__",    # Python cache
    ".git",           # Git repository
    ".venv",          # Virtual environment
    "node_modules",   # Node.js modules
    ".tox",           # Tox testing
    "build",          # Build artifacts
    "dist"            # Distribution files
]
```

### Custom File Filters

While not directly configurable via CLI, you can pre-filter files:

```bash
# Process only specific files
find ./src -name "*.py" -not -path "*/__pycache__/*" | \
    xargs -I {} dirname {} | sort | uniq | \
    xargs -I {} pyxplod {} ./output --method files
```

## Output Configuration

### Naming Conventions

#### Files Method Naming

```python
# Pattern: {original_stem}_{definition_name}.py
# Examples:
"utils.py" + "ConfigManager" → "utils_config_manager.py"
"helpers.py" + "format_data" → "helpers_format_data.py"
"api.py" + "APIClient" → "api_api_client.py"
```

#### Dirs Method Naming

```python
# Pattern: {definition_name}.py in {original_stem}/ directory
# Examples:
"utils.py" + "ConfigManager" → "utils/config_manager.py"
"helpers.py" + "format_data" → "helpers/format_data.py"
"api.py" + "APIClient" → "api/api_client.py"
```

### Path Resolution

```bash
# Input path resolution
./src → /absolute/path/to/src
../parent/src → /absolute/path/to/parent/src
/absolute/src → /absolute/src

# Output path creation
./output → Creates if doesn't exist
/tmp/exploded → Creates full path if needed
```

## Error Handling Configuration

### Error Recovery Modes

#### Strict Mode (Default)

```bash
# Stops on first critical error
pyxplod ./src ./out --method files
```

#### Tolerant Mode

```bash
# Continue processing despite errors
export PYXPLOD_CONTINUE_ON_ERROR=true
pyxplod ./src ./out --method files --verbose
```

### Error Reporting

```bash
# Detailed error reporting
pyxplod ./src ./out --method files --verbose 2>&1 | tee explosion.log

# Error summary only
pyxplod ./src ./out --method files 2>/dev/null
```

## Performance Configuration

### Processing Optimization

```bash
# Optimize for speed (files method)
export PYXPLOD_OPTIMIZE_SPEED=true
pyxplod ./src ./out --method files

# Optimize for organization (dirs method)  
export PYXPLOD_OPTIMIZE_ORGANIZATION=true
pyxplod ./src ./out --method dirs
```

### Memory Management

```bash
# Limit memory usage for large files
export PYXPLOD_MAX_MEMORY_MB=512

# Process files in batches
export PYXPLOD_BATCH_PROCESSING=true
```

## Integration Configuration

### Version Control Integration

```bash
# Create git-friendly output
export PYXPLOD_GIT_FRIENDLY=true

# Preserve file timestamps
export PYXPLOD_PRESERVE_TIMESTAMPS=true

# Generate .gitignore for exploded files
export PYXPLOD_GENERATE_GITIGNORE=true
```

### IDE Integration

```bash
# Generate IDE configuration files
export PYXPLOD_GENERATE_IDE_CONFIG=true

# Create import maps for IDEs
export PYXPLOD_GENERATE_IMPORT_MAPS=true
```

## Troubleshooting

### Common Configuration Issues

#### Issue: Permission Errors

```bash
# Problem
pyxplod ./src /root/output --method files
# Error: Permission denied

# Solution: Use accessible output directory
pyxplod ./src ./output --method files

# Or: Change permissions
sudo chown $USER:$USER /root/output
```

#### Issue: Path Not Found

```bash
# Problem
pyxplod ./nonexistent ./output --method files
# Error: Input directory does not exist

# Solution: Verify path exists
ls -la ./src
pyxplod ./src ./output --method files
```

#### Issue: No Python Files Found

```bash
# Problem
pyxplod ./empty_dir ./output --method files
# Warning: No Python files found

# Solution: Check directory contents
find ./src -name "*.py" -type f
```

### Debug Configuration

```bash
# Maximum debug output
export PYXPLOD_LOG_LEVEL=DEBUG
export PYXPLOD_TRACE_IMPORTS=true
export PYXPLOD_TRACE_AST=true
pyxplod ./src ./out --method files --verbose
```

### Validation Configuration

```bash
# Validate output after explosion
export PYXPLOD_VALIDATE_OUTPUT=true

# Check import integrity
export PYXPLOD_CHECK_IMPORTS=true

# Verify syntax of generated files
export PYXPLOD_VERIFY_SYNTAX=true
```

## Configuration Files

While pyxplod doesn't use configuration files by default, you can create wrapper scripts:

### `pyxplod-config.sh`

```bash
#!/bin/bash
# Default configuration for pyxplod

export PYXPLOD_LOG_LEVEL=INFO
export PYXPLOD_DEFAULT_METHOD=dirs
export PYXPLOD_CONTINUE_ON_ERROR=true

# Run pyxplod with defaults
pyxplod "${1:-./src}" "${2:-./exploded}" --method "${PYXPLOD_DEFAULT_METHOD}" "$@"
```

### `pyproject.toml` Integration

```toml
[tool.pyxplod]
default_method = "dirs"
verbose = true
continue_on_error = true
log_level = "INFO"

[tool.pyxplod.paths]
input = "./src"
output = "./exploded"

[tool.pyxplod.filters]
exclude_dirs = ["__pycache__", ".git", "build"]
include_patterns = ["*.py"]
```

## Next Steps

- Learn about [AST processing](ast-processing.md) internals
- Explore [file organization](file-organization.md) patterns
- Check the [API reference](api-reference.md) for programmatic configuration