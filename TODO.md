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



