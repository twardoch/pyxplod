# TODO

## ✅ COMPLETED: Scope Resolution Issue

The `dirs` method now properly handles module-level variables. The scope resolution has been implemented and tested successfully.

**What was fixed:**
- Added `find_module_variables()` function to detect module-level assignments like `console = Console()`
- Enhanced `write_extracted_file()` to include required module variables in extracted files
- Updated both `files` and `dirs` methods to pass module variables to extracted files
- Enhanced import filtering to include imports needed by module variables

**Example (now working correctly):**

Original file:
```python
from rich.console import Console
console = Console()

def my_function():
    console.print("Hello")  # console is now defined in extracted file
```

Extracted file now includes:
```python
from rich.console import Console
console = Console()

def my_function():
    console.print("Hello")  # ✅ console is properly defined
```

**Status**: ✅ **RESOLVED** - Scope resolution implemented in both `files` and `dirs` methods with comprehensive testing.

## ✅ COMPLETED: Codebase Refactoring (MVP)

The core `pyxplod.py` script has been refactored into a modular structure to improve maintainability and readability.

**What was done:**
- The monolithic `pyxplod.py` was broken down into the following modules:
  - `utils.py`: For common helper functions like `to_snake_case`.
  - `ast_utils.py`: For all AST (Abstract Syntax Tree) manipulation and analysis.
  - `file_utils.py`: For file system operations, path validation, and filename generation.
  - `processors.py`: Contains the core logic for `process_python_file` and `process_python_file_dirs`.
  - `cli.py`: Handles the command-line interface using `fire`, including the `main` function and logging setup.
- `pyxplod.py` itself is now a thin layer, primarily re-exporting `main` from `cli.py`.
- Imports and dependencies between these new modules have been updated.
- `__init__.py` and `__main__.py` have been updated to reflect the new location of `main`.

**Status**: ✅ **COMPLETED** - Refactoring of `pyxplod.py` into submodules is complete.