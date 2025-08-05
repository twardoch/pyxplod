# File Organization

Comprehensive guide to how pyxplod organizes output files, naming conventions, directory structures, and best practices for managing exploded codebases.

## Organization Principles

pyxplod follows consistent organizational principles across both explosion methods:

1. **Predictable Naming**: File names follow clear, systematic patterns
2. **Relative Path Preservation**: Input directory structure is maintained in output
3. **Import Consistency**: Generated imports follow Python conventions
4. **Self-Contained Modules**: Each extracted file is independently functional

## Files Method Organization

### Basic Structure

The files method creates sibling files alongside modified originals:

```
input/
└── module.py

output/
├── module.py                    # Modified original
├── module_class_name.py         # Extracted class
├── module_function_name.py      # Extracted function
└── module_another_class.py      # Another extracted class
```

### Naming Conventions

#### File Naming Pattern

```python
# Pattern: {original_stem}_{definition_name}.py
# Where definition_name is converted to snake_case

"utils.py" + "ConfigManager"     → "utils_config_manager.py"
"helpers.py" + "formatData"      → "helpers_format_data.py"
"api.py" + "HTTPClient"          → "api_http_client.py"
"main.py" + "run_app"            → "main_run_app.py"
```

#### Snake Case Conversion

```python
# Class names (PascalCase → snake_case)
"DatabaseManager"    → "database_manager"
"APIClient"          → "api_client"
"XMLParser"          → "xml_parser"
"HTTPSConnection"    → "https_connection"

# Function names (usually already snake_case)
"process_data"       → "process_data"
"validateInput"      → "validate_input"  # camelCase → snake_case
"parse_XML"          → "parse_xml"
```

### Complex Example

**Input structure:**
```
project/
├── core/
│   ├── __init__.py
│   ├── database.py
│   └── utils.py
└── api/
    ├── __init__.py
    └── client.py
```

**Output structure (files method):**
```
exploded/
├── core/
│   ├── __init__.py
│   ├── database.py
│   ├── database_connection_manager.py
│   ├── database_query_builder.py
│   ├── utils.py
│   ├── utils_format_response.py
│   └── utils_validate_input.py
└── api/
    ├── __init__.py
    ├── client.py
    ├── client_http_client.py
    ├── client_auth_handler.py
    └── client_rate_limiter.py
```

### Import Patterns

**Original file after explosion:**
```python
# core/database.py (modified)
from .database_connection_manager import ConnectionManager
from .database_query_builder import QueryBuilder

# Remaining module-level code
DEFAULT_TIMEOUT = 30
logger = get_logger(__name__)
```

**Extracted files:**
```python
# core/database_connection_manager.py
import asyncio
from typing import Optional

# Module variables used by this class
DEFAULT_TIMEOUT = 30

class ConnectionManager:
    def __init__(self, timeout: Optional[int] = None):
        self.timeout = timeout or DEFAULT_TIMEOUT
```

## Dirs Method Organization

### Basic Structure

The dirs method creates subdirectories for each original file:

```
input/
└── module.py

output/
└── module/
    ├── __init__.py              # Modified original content + imports
    ├── class_name.py            # Extracted class
    ├── function_name.py         # Extracted function
    └── another_class.py         # Another extracted class
```

### Directory and File Naming

#### Directory Naming

```python
# Directory names based on original file stem
"utils.py"       → "utils/"
"api_client.py"  → "api_client/"
"__init__.py"    → Handled with files method (special case)
"__main__.py"    → Handled with files method (special case)
```

#### File Naming Within Directories

```python
# Pattern: {definition_name}.py (snake_case)
"ConfigManager"  → "config_manager.py"
"formatData"     → "format_data.py"
"HTTPClient"     → "http_client.py"
"run_app"        → "run_app.py"
```

### Complex Example

**Input structure:**
```
project/
├── core/
│   ├── __init__.py
│   ├── database.py
│   └── utils.py
└── api/
    ├── __init__.py
    └── client.py
```

**Output structure (dirs method):**
```
exploded/
├── core/
│   ├── __init__.py                    # Special file, uses files method
│   ├── database/
│   │   ├── __init__.py                # Original content + imports
│   │   ├── connection_manager.py      # Extracted class
│   │   └── query_builder.py           # Extracted class
│   └── utils/
│       ├── __init__.py                # Original content + imports
│       ├── format_response.py         # Extracted function
│       └── validate_input.py          # Extracted function
└── api/
    ├── __init__.py                    # Special file, uses files method
    └── client/
        ├── __init__.py                # Original content + imports
        ├── http_client.py             # Extracted class
        ├── auth_handler.py            # Extracted class
        └── rate_limiter.py            # Extracted class
```

### `__init__.py` Generation

**Original file content:**
```python
# core/database.py
import asyncio
import logging
from typing import Optional, Dict

DATABASE_URL = "postgresql://localhost/db"
logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manages database connections."""
    pass

class QueryBuilder:
    """Builds SQL queries."""
    pass

def setup_database():
    """Initialize database connection."""
    logger.info(f"Connecting to {DATABASE_URL}")

# Module initialization
logger.info("Database module loaded")
```

**Generated `__init__.py`:**
```python
# core/database/__init__.py
import asyncio
import logging
from typing import Optional, Dict
from .connection_manager import ConnectionManager
from .query_builder import QueryBuilder

# Preserved module-level code
DATABASE_URL = "postgresql://localhost/db"
logger = logging.getLogger(__name__)

def setup_database():
    """Initialize database connection."""
    logger.info(f"Connecting to {DATABASE_URL}")

# Module initialization
logger.info("Database module loaded")
```

## Special File Handling

### `__init__.py` Files

Package initialization files receive special treatment:

```python
# Always processed with files method, regardless of --method setting
# Prevents creation of __init__/__init__.py structures
# Preserves package initialization behavior
```

**Example:**
```
input/
└── package/
    └── __init__.py

# Both methods produce:
output/
└── package/
    ├── __init__.py                    # Modified original
    ├── __init___some_class.py         # Extracted class (files method)
    └── __init___some_function.py      # Extracted function (files method)
```

### `__main__.py` Files

Module entry points also get special handling:

```python
# Always use files method to preserve execution behavior
# Maintains compatibility with python -m package
```

**Example:**
```
input/
└── mypackage/
    └── __main__.py

# Both methods produce:
output/
└── mypackage/
    ├── __main__.py                    # Modified original
    ├── __main___main_function.py      # Extracted function
    └── __main___cli_handler.py        # Extracted class
```

## Name Collision Handling

### Collision Detection

pyxplod detects and resolves potential file name collisions:

```python
# Original files that could create conflicts
"utils.py" + "format_data" → "utils_format_data.py"
"utils_format.py" + "data" → "utils_format_data.py"  # Collision!
```

### Resolution Strategy

```python
# Collision resolution by adding numeric suffix
"utils_format_data.py"     # First file
"utils_format_data_1.py"   # Second file (collision resolved)
"utils_format_data_2.py"   # Third file (if needed)
```

### Logging Collisions

```bash
# Collision warnings in verbose mode
pyxplod ./src ./output --method files --verbose

# Output:
# WARNING | Name collision detected: utils_format_data.py
# INFO    | Resolved to: utils_format_data_1.py
```

## Directory Structure Preservation

### Relative Path Maintenance

Input directory structure is preserved in output:

**Input:**
```
project/
├── src/
│   ├── core/
│   │   ├── database.py
│   │   └── utils.py
│   └── api/
│       └── client.py
└── tests/
    └── test_core.py
```

**Output (files method):**
```
exploded/
├── src/
│   ├── core/
│   │   ├── database.py
│   │   ├── database_connection.py
│   │   ├── database_query.py
│   │   ├── utils.py
│   │   └── utils_helpers.py
│   └── api/
│       ├── client.py
│       └── client_http_client.py
└── tests/
    ├── test_core.py
    └── test_core_test_database.py
```

### Path Resolution

```python
# Input path: ./project/src/core/database.py
# Base input: ./project
# Relative path: src/core/database.py
# Output path: ./exploded/src/core/database.py
```

## Import Management

### Relative Import Generation

pyxplod generates appropriate relative imports:

```python
# Files method imports (sibling files)
from .module_class_name import ClassName
from .module_function_name import function_name

# Dirs method imports (from subdirectory)
from .module.class_name import ClassName
from .module.function_name import function_name
```

### Import Path Calculation

```python
# For files method
original_file = "src/core/database.py"
extracted_file = "src/core/database_connection.py"
import_statement = "from .database_connection import ConnectionManager"

# For dirs method  
original_package = "src/core/database/"
extracted_file = "src/core/database/connection.py"
import_statement = "from .connection import ConnectionManager"
```

### Cross-Directory Imports

External imports remain unchanged:

```python
# Original imports preserved
import os
import json
from pathlib import Path
from typing import Dict, List

# External project imports preserved
from ..utils import helper_function
from ...config import settings
```

## Best Practices

### Choosing Organization Method

#### Use Files Method When:

- **Small modules** (< 10 definitions)
- **Simple projects** with flat structure
- **Legacy code** requiring minimal structural change
- **Quick refactoring** needs

#### Use Dirs Method When:

- **Large modules** (> 10 definitions)
- **Complex projects** requiring better organization
- **Team projects** where clear structure aids collaboration
- **Future-oriented** projects planning further modularization

### File Naming Best Practices

```python
# Good: Clear, descriptive names
utils_data_processor.py
api_http_client.py
config_database_settings.py

# Avoid: Ambiguous or overly long names
utils_thing.py                    # Too vague
api_hypertext_transfer_protocol_client_implementation.py  # Too long
```

### Directory Organization

```python
# Good: Logical grouping
src/
├── core/
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   └── query.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
└── api/
    └── client/
        ├── __init__.py
        └── http.py

# Avoid: Overly nested or flat structures
src/database_connection_manager.py      # Too flat
src/core/db/conn/mgr/pool/handler.py   # Too nested
```

## Troubleshooting Organization Issues

### Common Problems

#### Problem: Import Errors After Explosion

```python
# Before explosion
from utils import helper_function

# After explosion - may need updating
from utils_helper_function import helper_function
```

**Solution:** Check import statements and update if necessary.

#### Problem: Circular Import Dependencies

```python
# module_a.py imports from module_b_class.py
# module_b_class.py imports from module_a.py
```

**Solution:** Identify and refactor circular dependencies before explosion.

#### Problem: Missing Module Variables

```python
# Variable used but not included in extracted file
CONFIG_PATH = "/etc/config"  # Missing in extracted file

class ConfigManager:
    def __init__(self):
        self.path = CONFIG_PATH  # NameError!
```

**Solution:** pyxplod should handle this automatically; check for bugs or edge cases.

### Debugging Organization

```bash
# Enable verbose logging to see organization decisions
pyxplod ./src ./output --method dirs --verbose

# Check generated file structure
tree ./output

# Validate imports in generated files
python -m py_compile output/**/*.py
```

## Next Steps

Understanding file organization helps you:

- **Plan explosion strategy** based on project structure
- **Predict output structure** before running pyxplod
- **Organize exploded code** effectively
- **Troubleshoot organization issues**

Continue with:
- [API Reference](api-reference.md) - Programmatic access to organization functions
- [CLI Usage](cli-usage.md) - Command-line options affecting organization