# Quick Start Guide

Get up and running with pyxplod in minutes! This guide walks you through your first code explosion.

## Basic Usage

The simplest way to use pyxplod:

```bash
pyxplod input_directory output_directory --method files
```

### Real Example

Let's explode a sample Python project:

1. **Create a sample project**:
```bash
mkdir my_project
cd my_project
```

2. **Create a Python file** (`utils.py`):
```python
"""Utility functions and classes."""

import os
import json
from pathlib import Path

# Module-level constant
DEFAULT_CONFIG = {"debug": False, "version": "1.0"}

class ConfigManager:
    """Manages application configuration."""
    
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.config = DEFAULT_CONFIG.copy()
    
    def load(self):
        """Load configuration from file."""
        if self.config_path.exists():
            with open(self.config_path) as f:
                self.config.update(json.load(f))

def format_output(data: dict) -> str:
    """Format data for console output."""
    return json.dumps(data, indent=2)

def validate_path(path_str: str) -> bool:
    """Validate if path exists and is accessible."""
    path = Path(path_str)
    return path.exists() and os.access(path, os.R_OK)
```

3. **Run pyxplod**:
```bash
pyxplod my_project exploded_project --method files --verbose
```

## What Happens?

After running pyxplod, your `exploded_project` directory will contain:

```
exploded_project/
├── utils.py                    # Modified original file
├── utils_config_manager.py     # Extracted ConfigManager class
├── utils_format_output.py      # Extracted format_output function
└── utils_validate_path.py      # Extracted validate_path function
```

### Modified Original File (`utils.py`)

```python
"""Utility functions and classes."""

import os
import json
from pathlib import Path
from .utils_config_manager import ConfigManager
from .utils_format_output import format_output
from .utils_validate_path import validate_path

# Module-level constant (preserved)
DEFAULT_CONFIG = {"debug": False, "version": "1.0"}
```

### Extracted Files

**`utils_config_manager.py`:**
```python
import json
from pathlib import Path

# Module variables used by this class
DEFAULT_CONFIG = {"debug": False, "version": "1.0"}

class ConfigManager:
    """Manages application configuration."""
    
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.config = DEFAULT_CONFIG.copy()
    
    def load(self):
        """Load configuration from file."""
        if self.config_path.exists():
            with open(self.config_path) as f:
                self.config.update(json.load(f))
```

**`utils_format_output.py`:**
```python
import json

def format_output(data: dict) -> str:
    """Format data for console output."""
    return json.dumps(data, indent=2)
```

## Method Comparison

### Files Method (`--method files`)

- Creates sibling files with naming pattern: `original_extracted_name.py`
- Best for simple extraction and flat structures
- Original file imports from sibling files

**Example structure:**
```
project/
├── module.py
├── module_my_class.py
├── module_my_function.py
└── module_helper.py
```

### Dirs Method (`--method dirs`)

- Creates subdirectories for each original file
- Places extracted components in subdirectory
- Creates `__init__.py` with imports and remaining code

**Example structure:**
```
project/
└── module/
    ├── __init__.py          # Imports + remaining code
    ├── my_class.py
    ├── my_function.py
    └── helper.py
```

Try both methods to see which fits your project structure better!

## Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `--method` | Explosion method: `files` or `dirs` | `files` |
| `--verbose` | Enable detailed logging | `False` |

## Best Practices

1. **Start Small**: Test on a small project first
2. **Backup Original**: Always keep a backup of your original code
3. **Use Version Control**: Commit before exploding to track changes
4. **Review Output**: Check extracted files for correctness
5. **Test Functionality**: Ensure your code still works after explosion

## Common Use Cases

- **Legacy Code Refactoring**: Break down large, monolithic modules
- **Project Reorganization**: Improve code structure and maintainability  
- **Module Splitting**: Separate concerns into focused files
- **Code Review Preparation**: Make large files easier to review

## Next Steps

- Learn about the [core concepts](concepts.md) behind pyxplod
- Explore different [methods and strategies](methods.md)
- Check the [full CLI reference](cli-usage.md) for advanced options

Ready to explode some code? 🧨