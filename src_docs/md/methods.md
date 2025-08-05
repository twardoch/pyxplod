# Methods & Strategies

pyxplod offers two primary explosion methods, each suited for different project structures and organizational preferences. This chapter provides detailed comparisons and guidance for choosing the right method.

## Overview of Methods

| Aspect | Files Method | Dirs Method |
|--------|-------------|-------------|
| **Output Structure** | Sibling files | Subdirectories |
| **File Naming** | `original_name_definition.py` | `definition.py` |
| **Import Style** | Relative imports from siblings | Imports from subdirectory |
| **Best For** | Simple extraction, flat structures | Complex modules, namespace organization |
| **`__init__.py` Files** | Not created | Created with imports + remaining code |

## Files Method (`--method files`)

The files method extracts definitions to sibling files alongside the original.

### Structure Example

**Before explosion:**
```
project/
└── utils.py
```

**After explosion:**
```
project/
├── utils.py                    # Modified original
├── utils_config_manager.py     # Extracted class
├── utils_helper_function.py    # Extracted function
└── utils_data_processor.py     # Extracted class
```

### How It Works

1. **Extract each definition** to a new file with pattern `{original}_{definition}.py`
2. **Modify original file** to import from the new files
3. **Preserve module-level code** in the original file

### Example Transformation

**Original (`utils.py`):**
```python
import json
from pathlib import Path

CONFIG_FILE = "config.json"

class ConfigManager:
    def __init__(self):
        self.config_file = Path(CONFIG_FILE)
    
    def load(self):
        with open(self.config_file) as f:
            return json.load(f)

def format_data(data):
    return json.dumps(data, indent=2)

# Module-level initialization
print("Utils module loaded")
```

**After explosion:**

**`utils.py` (modified):**
```python
from .utils_config_manager import ConfigManager
from .utils_format_data import format_data

# Preserved module-level code
CONFIG_FILE = "config.json"
print("Utils module loaded")
```

**`utils_config_manager.py` (new):**
```python
import json
from pathlib import Path

# Module variables used by this class
CONFIG_FILE = "config.json"

class ConfigManager:
    def __init__(self):
        self.config_file = Path(CONFIG_FILE)
    
    def load(self):
        with open(self.config_file) as f:
            return json.load(f)
```

**`utils_format_data.py` (new):**
```python
import json

def format_data(data):
    return json.dumps(data, indent=2)
```

### Advantages

- **Simple structure**: Easy to understand and navigate
- **Minimal changes**: Original file structure mostly preserved
- **Flat hierarchy**: No nested directories to manage
- **Direct imports**: Clear import relationships

### Disadvantages

- **Name collision risk**: Many files with similar prefixes
- **Cluttered directories**: Can create many files in one location
- **Limited organization**: No grouping of related components

### Best Use Cases

- **Small to medium modules** with few definitions
- **Projects with flat structure** preferences
- **Quick refactoring** where minimal structural change is desired
- **Legacy code** where directory structure changes are risky

## Dirs Method (`--method dirs`)

The dirs method creates subdirectories for each original file, organizing extracted components within.

### Structure Example

**Before explosion:**
```
project/
└── utils.py
```

**After explosion:**
```
project/
└── utils/
    ├── __init__.py           # Imports + remaining code
    ├── config_manager.py     # Extracted class
    ├── format_data.py        # Extracted function  
    └── data_processor.py     # Extracted class
```

### How It Works

1. **Create subdirectory** named after the original file (without `.py`)
2. **Extract definitions** to individual files in the subdirectory
3. **Generate `__init__.py`** with imports and remaining module-level code
4. **Handle special files** (`__init__.py`, `__main__.py`) using files method

### Example Transformation

**Original (`utils.py`):**
```python
import json
from pathlib import Path

CONFIG_FILE = "config.json"

class ConfigManager:
    def __init__(self):
        self.config_file = Path(CONFIG_FILE)

def format_data(data):
    return json.dumps(data, indent=2)

def validate_config():
    return Path(CONFIG_FILE).exists()

# Module initialization
_initialized = False
if not _initialized:
    print("Utils module loaded")
    _initialized = True
```

**After explosion:**

**`utils/__init__.py` (new):**
```python
import json
from pathlib import Path
from .config_manager import ConfigManager
from .format_data import format_data
from .validate_config import validate_config

# Preserved module-level code
CONFIG_FILE = "config.json"
_initialized = False
if not _initialized:
    print("Utils module loaded")
    _initialized = True
```

**`utils/config_manager.py` (new):**
```python
from pathlib import Path

# Module variables used by this class
CONFIG_FILE = "config.json"

class ConfigManager:
    def __init__(self):
        self.config_file = Path(CONFIG_FILE)
```

**`utils/format_data.py` (new):**
```python
import json

def format_data(data):
    return json.dumps(data, indent=2)
```

### Advantages

- **Clean organization**: Related components grouped in directories
- **Namespace preservation**: Original module name becomes package
- **Scalability**: Better for modules with many definitions
- **Clear separation**: Physical separation of concerns

### Disadvantages

- **More complex structure**: Additional directories to manage
- **Import complexity**: Slightly more complex import paths
- **Package conversion**: Changes modules into packages

### Best Use Cases

- **Large modules** with many classes and functions
- **Projects favoring organization** over simplicity
- **Team environments** where clear structure aids collaboration
- **API modules** where namespace organization is valuable

## Special File Handling

### `__init__.py` Files

Both methods handle `__init__.py` files specially:

- **Always use files method logic** (even when `--method dirs` is specified)
- **Prevent creation** of `__init__/__init__.py` structures
- **Preserve package initialization** behavior

### `__main__.py` Files

Similar special handling for entry point files:

- **Use files method** to avoid structural complications
- **Maintain execution behavior** when run as `python -m package`

## Choosing the Right Method

### Use Files Method When:

- ✅ Working with **small to medium files** (< 10 definitions)
- ✅ Prefer **minimal structural changes**
- ✅ Need **simple, flat organization**
- ✅ Working with **legacy code** requiring careful changes
- ✅ Team prefers **straightforward imports**

### Use Dirs Method When:

- ✅ Dealing with **large modules** (> 10 definitions)
- ✅ Want **better organization** and namespace management
- ✅ Working on **new projects** where structure changes are welcome
- ✅ Need **clear separation** of concerns
- ✅ Planning **further modularization**

## Hybrid Approaches

### Method Selection by File

You can apply different methods to different files:

```bash
# Use files method for specific files
pyxplod src/small_utils.py output/ --method files

# Use dirs method for complex modules  
pyxplod src/large_module.py output/ --method dirs
```

### Iterative Explosion

Start with files method, then reorganize:

1. **First pass**: Use files method for quick extraction
2. **Review**: Identify related components
3. **Second pass**: Use dirs method or manual reorganization

## Performance Considerations

### Files Method
- **Faster processing**: Simpler file operations
- **Less disk space**: No additional directories
- **Simpler cleanup**: Fewer files to manage

### Dirs Method  
- **Slightly slower**: More directory operations
- **More organized**: Better long-term maintainability
- **Package benefits**: Can leverage Python package features

## Next Steps

- Learn about [command-line usage](cli-usage.md) for applying these methods
- Explore [file organization](file-organization.md) patterns in detail
- Check [configuration options](configuration.md) for fine-tuning behavior