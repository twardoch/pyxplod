# PLAN.md

## Alternative Implementation: --method dirs

### Overview
The `--method dirs` option provides an alternative way to explode Python files. Instead of creating separate files in the same directory (default `--method files` behavior), this method creates a subfolder for each Python file and organizes the extracted code differently.

### Specification for --method dirs

When using `--method dirs`, pyxplod will:

1. **Convert each .py file to a directory** with the same name (without .py extension)
2. **Extract each class and function** into separate .py files within that directory
3. **Create an `__init__.py`** containing:
   - All module-level imports from the original file
   - Imports for all extracted classes/functions
   - Any remaining module-level code (constants, module variables, etc.)

### Example Transformation (--method dirs)

Input: `src/utils.py`
```python
import os
from typing import List

CONSTANT = "value"

class MyClass:
    def method(self):
        pass

def my_function():
    pass

# Module-level code
print("Module loaded")
```

Output structure:
```
output/
└── src/
    └── utils/
        ├── __init__.py
        ├── my_class.py
        └── my_function.py
```

**output/src/utils/__init__.py:**
```python
import os
from typing import List

from .my_class import MyClass
from .my_function import my_function

CONSTANT = "value"

# Module-level code
print("Module loaded")
```

**output/src/utils/my_class.py:**
```python
import os
from typing import List

class MyClass:
    def method(self):
        pass
```

**output/src/utils/my_function.py:**
```python
import os
from typing import List

def my_function():
    pass
```

### Implementation Details for --method dirs

1. **Directory Creation**: Each .py file becomes a package (directory with __init__.py)
2. **Import Handling**: The __init__.py re-exports all extracted components to maintain API compatibility
3. **Naming**: Use simple snake_case names without the original filename prefix
4. **Compatibility**: External imports remain unchanged: `from src.utils import MyClass` still works

---

## pyxplod Implementation Plan

### Overview
`pyxplod` is a Python tool that deterministically "explodes" a Python project by extracting classes and functions into separate files and replacing them with imports.

### Current Implementation Status

The core `pyxplod` functionality has been implemented with the following features:

- ✅ CLI interface using `fire` with `--input`, `--output`, `--method`, and `--verbose` flags
- ✅ Two extraction methods: `files` (default) and `dirs`
- ✅ Recursive Python file discovery with proper filtering
- ✅ AST-based parsing and modification
- ✅ Class and function extraction with snake_case naming
- ✅ Automatic import generation and replacement
- ✅ Import optimization - only includes imports actually used in extracted files
- ✅ Error handling for syntax errors and edge cases
- ✅ Progress bars and logging with `loguru` and `rich`
- ✅ Comprehensive test suite (79% coverage)

### Remaining Implementation Tasks

- [ ] **Phase 1: Critical Fixes & Improvements** (High Priority)
  - [ ] Preserve decorators and docstrings properly in extracted files
  - [ ] Handle comments between definitions (currently lost)
  - [ ] Add proper encoding handling for Unicode files
  - [ ] Improve error recovery - partial processing instead of skipping entirely
  - [ ] Fix import statement positioning relative to docstrings

- [ ] **Phase 2: Code Quality & Architecture** (Medium Priority)
  - [ ] Refactor `pyxplod.py` into multiple modules (currently 450+ lines):
    - `ast_utils.py` - AST manipulation functions
    - `file_utils.py` - File discovery and I/O operations
    - `processors.py` - Processing method implementations (files/dirs)
    - `cli.py` - Command line interface
  - [ ] Add comprehensive type hints using simple syntax (list, dict, |)
  - [ ] Implement proper debug logging patterns per CLAUDE.md
  - [ ] Add integration tests with real Python projects

- [ ] **Phase 3: Essential User Features** (Medium Priority)
  - [ ] Add `--dry-run` flag to preview changes without writing files
  - [ ] Support `.pyxplod.toml` configuration file
  - [ ] Handle nested classes and inner functions
  - [ ] Add `--exclude` pattern for skipping files/directories
  - [ ] Add `--include-private` flag for private methods/classes

- [ ] **Phase 4: Advanced Features** (Low Priority)
  - [ ] Add `--format` option to preserve formatting using Black
  - [ ] Support for async function annotations and decorators
  - [ ] Handle complex decorator chains (@property, @classmethod, etc.)
  - [ ] Implement reverse operation (`--method implode` to merge files back)
  - [ ] Add `--verify` flag to validate output integrity

- [ ] **Phase 5: Performance & Scalability** (Future)
  - [ ] Parallel processing using multiprocessing for large codebases
  - [ ] Streaming AST processing for very large files
  - [ ] Incremental mode - only process changed files since last run
  - [ ] Memory-efficient processing for huge codebases
  - [ ] Progress persistence for resumable operations

- [ ] **Phase 6: Testing & Documentation** (Ongoing)
  - [ ] Add property-based testing with Hypothesis
  - [ ] Create test suite with popular Python projects (requests, flask, etc.)
  - [ ] Add performance benchmarks and profiling
  - [ ] Generate API documentation with Sphinx
  - [ ] Add visual examples and before/after diagrams

### Technical Decisions

1. **AST vs. Regular Expressions**: Use AST for accurate parsing and modification
2. **Import Style**: Use relative imports for split files to maintain portability
3. **Naming Convention**: Snake_case with deduplication to avoid conflicts
4. **Error Handling**: Fail gracefully, skip problematic files with warnings
5. **Logging**: Verbose mode with loguru for debugging

### Dependencies Required
- `fire` - CLI interface
- `loguru` - Enhanced logging
- `ast` - Python AST parsing (built-in)
- `pathlib` - Path operations (built-in)

### Example Transformations

#### Method: files (default)

Input: `src/utils.py`
```python
import os

class MyClass:
    def method(self):
        pass

def my_function():
    pass
```

Output:
```
output/src/
├── utils.py
├── utils_my_class.py
└── utils_my_function.py
```

#### Method: dirs

Same input produces:
```
output/src/
└── utils/
    ├── __init__.py
    ├── my_class.py
    └── my_function.py
```

Both methods maintain API compatibility - external code using `from src.utils import MyClass` continues to work unchanged.

### Known Issues & Limitations

1. **Lost Elements**: Comments between definitions and some formatting are not preserved
2. **Limited Scope**: Only handles top-level classes and functions, not nested definitions
3. **Formatting**: Uses `ast.unparse()` which doesn't preserve original code formatting
4. **Memory Usage**: Entire AST is kept in memory, could be problematic for very large files
5. **Error Handling**: Files with syntax errors are skipped entirely instead of partial processing
6. **Decorator Preservation**: Some decorators may not be properly preserved in extracted files

### Design Decisions & Rationale

1. **Two Methods Approach**: 
   - `files` method: Simple, flat structure, good for small modules
   - `dirs` method: Package structure, better for larger modules, cleaner imports

2. **AST-based Processing**: Ensures syntactic correctness and proper Python structure

3. **Import Strategy**: Currently copies all imports for safety, needs optimization

4. **Naming Convention**: Snake_case with deduplication ensures filesystem compatibility

5. **Error Philosophy**: Fail safely, skip problematic files with clear error messages