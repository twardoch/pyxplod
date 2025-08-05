# Understanding Explosion

This chapter explains the core concepts behind pyxplod's code explosion process and how it transforms your Python projects.

## What is Code Explosion?

**Code explosion** is the process of breaking down monolithic Python files by extracting top-level classes and functions into separate, self-contained modules. This creates a more modular structure while preserving functionality.

### The Problem

Large Python files often contain:
- Multiple unrelated classes
- Various utility functions  
- Mixed concerns and responsibilities
- Difficult-to-navigate code
- Complex import dependencies

### The Solution

pyxplod systematically extracts each top-level definition into its own file, creating:
- **Focused modules** with single responsibilities
- **Clear dependencies** through explicit imports
- **Easier navigation** with smaller files
- **Better maintainability** through separation of concerns

## How pyxplod Works

### 1. AST Analysis

pyxplod uses Python's **Abstract Syntax Tree (AST)** to understand your code structure:

```python
import ast

# pyxplod parses your file into an AST
with open('module.py', 'r') as f:
    tree = ast.parse(f.read())

# Then analyzes top-level definitions
for node in ast.walk(tree):
    if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
        # Extract this definition
        process_definition(node)
```

### 2. Dependency Detection

For each extracted definition, pyxplod identifies:

- **Used names**: Variables, functions, classes referenced
- **Required imports**: External modules and packages needed
- **Module variables**: Constants and globals used by the definition

### 3. Smart Import Filtering

Only necessary imports are included in extracted files:

**Original file (`utils.py`):**
```python
import os
import sys
import json
from pathlib import Path
from typing import Dict, List

def process_file(filepath: str) -> Dict:
    """Only uses os, json, and Path."""
    path = Path(filepath)
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)
```

**Extracted file (`utils_process_file.py`):**
```python
import os
import json
from pathlib import Path
from typing import Dict

def process_file(filepath: str) -> Dict:
    """Only uses os, json, and Path."""
    path = Path(filepath)
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)
```

Notice how `sys` and `List` imports are excluded because they're not used.

### 4. Module Variable Handling

When extracted code uses module-level variables, they're included:

**Original:**
```python
# config.py
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3

class APIClient:
    def __init__(self):
        self.timeout = DEFAULT_TIMEOUT
        self.retries = MAX_RETRIES
```

**Extracted (`config_api_client.py`):**
```python
# Module variables used by this class
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3

class APIClient:
    def __init__(self):
        self.timeout = DEFAULT_TIMEOUT
        self.retries = MAX_RETRIES
```

## Key Principles

### 1. Preservation of Functionality

pyxplod **never** changes the behavior of your code:
- All imports are preserved where needed
- Module variables are copied to extracted files
- Original file structure remains valid

### 2. Self-Contained Modules

Each extracted file is **completely independent**:
- Contains all necessary imports
- Includes required module variables
- Can be imported and used standalone

### 3. Minimal Imports

Only **essential imports** are included:
- Unused imports are filtered out
- Import aliases are preserved
- Relative imports are maintained

### 4. Naming Consistency

File naming follows predictable patterns:
- **Files method**: `original_definition_name.py`
- **Dirs method**: `definition_name.py` in subdirectory

## AST Processing Deep Dive

### Definition Extraction

pyxplod identifies these top-level constructs:

```python
# Classes
class MyClass:
    pass

# Functions  
def my_function():
    pass

# Async functions
async def async_function():
    pass

# Methods (when at module level)
@classmethod
def class_method(cls):
    pass
```

### Name Usage Analysis

For each definition, pyxplod analyzes:

1. **Direct references**: Variables used in the function/class body
2. **Nested references**: Names used in nested functions or methods
3. **Decorator references**: Names used in decorators
4. **Type annotations**: Names used in type hints

### Import Resolution

pyxplod handles various import styles:

```python
import os                    # → import os
import os.path               # → import os.path  
from pathlib import Path     # → from pathlib import Path
from . import utils          # → from . import utils (relative)
from ..parent import helper  # → from ..parent import helper
import numpy as np           # → import numpy as np (alias)
```

## Explosion Strategies

### Conservative Approach

pyxplod takes a **conservative approach** to ensure safety:

- Only extracts top-level definitions
- Preserves all potentially needed imports
- Maintains original code comments
- Keeps module docstrings

### Error Handling

If pyxplod encounters issues:

- **Syntax errors**: File is skipped with error message
- **Import conflicts**: Original imports are preserved
- **Circular dependencies**: Handled through careful import management
- **Special files**: `__init__.py`, `__main__.py` handled differently

## Benefits of Understanding These Concepts

1. **Predictable Results**: Know what to expect from explosion
2. **Debugging**: Understand why certain imports are included
3. **Customization**: Make informed decisions about explosion methods
4. **Troubleshooting**: Identify and resolve issues more effectively

## Next Steps

Now that you understand the core concepts, explore:
- [Methods & Strategies](methods.md) - Different explosion approaches
- [AST Processing](ast-processing.md) - Technical implementation details
- [File Organization](file-organization.md) - Output structure patterns