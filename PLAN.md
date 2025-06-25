# PLAN.md

## Critical Scope Resolution Issue (URGENT)

**Problem**: When extracting functions/classes with the `dirs` method, module-level variables are not included in extracted files, causing `NameError` in the extracted code.

**Example**:
```python
# Original file
from rich.console import Console
console = Console()

def my_function():
    console.print("Hello")  # 'console' undefined in extracted file
```

**Solution Strategy**:
1. **Detect Module-Level Variables**: Identify assignments like `console = Console()` at module level
2. **Analyze Dependencies**: Check which extracted definitions reference these variables
3. **Include Required Variables**: Copy necessary module-level assignments to extracted files
4. **Maintain Import Order**: Ensure variables come after their required imports

**Implementation Plan**:
- [x] Add `find_module_variables()` function to detect module-level assignments
- [x] Enhance `analyze_name_usage()` to distinguish between imported names and module variables
- [x] Update `write_extracted_file()` to include required module variables
- [x] Apply fix to both `files` and `dirs` methods
- [x] Test with rich.console example from TODO.md

**Status**: ✅ **COMPLETED** - Scope resolution implemented and tested successfully.

## Sprint 2

### Code Quality & Preservation Issues
- [ ] **Fix code element preservation** (HIGH PRIORITY)
  - [ ] Maintain decorators on extracted functions/classes (@property, @staticmethod, etc.)
  - [ ] Preserve docstrings in correct positions (before or after imports)
  - [ ] Handle comments between definitions (currently lost during AST processing)
  - [ ] Ensure type annotations are preserved exactly

### Error Handling & Robustness  
- [ ] **Improve error handling and Unicode support**
  - [ ] Add proper Unicode/encoding support (UTF-8, other encodings)
  - [ ] Implement partial file processing on syntax errors
  - [ ] Better error messages with file names and line numbers
  - [ ] Add `--skip-errors` flag to continue processing despite errors

## Next Sprint - Architecture & Features (v0.5.0)

### Code Architecture
- [x] **Refactor monolithic pyxplod.py** (Completed)
  - [x] Extract `utils.py` - Common utility functions (e.g., `to_snake_case`)
  - [x] Extract `ast_utils.py` - AST manipulation and analysis functions
  - [x] Extract `file_utils.py` - File discovery, I/O, and path operations
  - [x] Extract `processors.py` - Method implementation logic (files/dirs)
  - [x] Extract `cli.py` - Command line interface and argument parsing, `main` function

### Type System & Documentation
- [ ] **Enhance type system**
  - [ ] Add comprehensive type hints using simple syntax (list, dict, str | None)
  - [ ] Use proper AST node types instead of generic types
  - [ ] Add return type annotations to all functions

### User Experience Features
- [ ] **Essential user features**
  - [ ] Add `--dry-run` mode to preview changes without writing files
  - [ ] Create `.pyxplod.toml` configuration file support
  - [ ] Add `--exclude` patterns for skipping files/directories
  - [ ] Add `--include-private` flag for private methods/classes

## Future Backlog

### Advanced Code Handling
- [ ] **Complex code structures**
  - [ ] Handle nested classes and inner functions
  - [ ] Support async functions and async decorators
  - [ ] Handle complex decorator chains (@property, @classmethod, @lru_cache)
  - [ ] Support class methods, static methods, and property decorators

### Testing & Quality Assurance
- [ ] **Expand test coverage**
  - [ ] Test decorator preservation with various decorator types
  - [ ] Test Unicode file handling with different encodings
  - [ ] Test large file processing (>1000 lines)
  - [ ] Test error conditions and edge cases
  - [ ] Add integration tests with popular packages (requests, flask, django)

### Performance & Scalability
- [ ] **Performance improvements**
  - [ ] Implement parallel file processing for large codebases
  - [ ] Add streaming AST processing for very large files
  - [ ] Create incremental mode - only process changed files
  - [ ] Add progress persistence for resumable operations

### Advanced Features
- [ ] **Professional tooling features**
  - [ ] Add `--format` flag with Black integration for code formatting
  - [ ] Add `--verify` flag to validate output file integrity
  - [ ] Implement reverse operation (`--method implode`) to merge files back
  - [ ] Create plugin system for custom processing logic

### Documentation & Examples
- [ ] **Improve documentation**
  - [ ] Add inline comments explaining complex AST operations
  - [ ] Document import analysis and filtering logic
  - [ ] Create examples directory with before/after transformations
  - [ ] Add visual diagrams showing both processing methods



### Remaining Implementation Tasks

- [ ] **Phase 1: Critical Fixes & Improvements** (High Priority)
  - [ ] Preserve decorators and docstrings properly in extracted files
  - [ ] Handle comments between definitions (currently lost)
  - [ ] Add proper encoding handling for Unicode files
  - [ ] Improve error recovery - partial processing instead of skipping entirely
  - [ ] Fix import statement positioning relative to docstrings

- [x] **Phase 2: Code Quality & Architecture** (Completed for refactoring part)
  - [x] Refactor `pyxplod.py` into multiple modules:
    - `utils.py` - Common utility functions (e.g., `to_snake_case`)
    - `ast_utils.py` - AST manipulation functions
    - `file_utils.py` - File discovery and I/O operations
    - `processors.py` - Processing method implementations (files/dirs)
    - `cli.py` - Command line interface and `main` function
  - [ ] Add comprehensive type hints using simple syntax (list, dict, |) (Ongoing)
  - [ ] Implement proper debug logging patterns per CLAUDE.md (Partially addressed)
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