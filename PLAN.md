# PLAN.md

## pyxplod Implementation Plan

### Overview
`pyxplod` is a Python tool that deterministically "explodes" a Python project by extracting classes and functions into separate files and replacing them with imports.

### Detailed Implementation Steps

- [ ] **Phase 1: Core Infrastructure**
  - [ ] Set up CLI interface using `fire` library
  - [ ] Add `--input` and `--output` command-line arguments
  - [ ] Add `--verbose` flag for debug logging
  - [ ] Set up loguru-based logging system
  - [ ] Validate input/output paths exist and are accessible

- [ ] **Phase 2: File Discovery**
  - [ ] Implement recursive Python file discovery using `pathlib`
  - [ ] Filter for `.py` files only
  - [ ] Maintain relative path structure for output
  - [ ] Skip `__pycache__` and other Python metadata directories

- [ ] **Phase 3: AST Processing**
  - [ ] Parse each Python file into AST using `ast` module
  - [ ] Identify all class definitions (`ast.ClassDef`)
  - [ ] Identify all function definitions (`ast.FunctionDef`)
  - [ ] Extract import statements to preserve in split files
  - [ ] Handle nested classes and functions appropriately

- [ ] **Phase 4: File Generation**
  - [ ] Create naming convention: `original_filename_class_or_function_name.py`
  - [ ] Convert class/function names to snake_case
  - [ ] Handle name deduplication if conflicts arise
  - [ ] Create output directory structure mirroring input
  - [ ] Generate new files with proper imports and definitions

- [ ] **Phase 5: AST Modification**
  - [ ] Replace class/function definitions with relative imports
  - [ ] Calculate correct relative import paths
  - [ ] Preserve module-level code and imports
  - [ ] Handle docstrings and decorators correctly
  - [ ] Maintain proper Python syntax in modified files

- [ ] **Phase 6: File Writing**
  - [ ] Write modified AST back to Python code using `ast.unparse()`
  - [ ] Preserve formatting as much as possible
  - [ ] Create output directory structure
  - [ ] Write all generated files with proper permissions
  - [ ] Handle file conflicts gracefully

- [ ] **Phase 7: Edge Cases & Error Handling**
  - [ ] Handle empty files
  - [ ] Handle files with only imports
  - [ ] Handle syntax errors in input files
  - [ ] Handle circular dependencies
  - [ ] Handle files with no classes/functions
  - [ ] Add proper error messages and recovery

- [ ] **Phase 8: Testing & Documentation**
  - [ ] Write unit tests for each component
  - [ ] Create integration tests with sample projects
  - [ ] Test edge cases
  - [ ] Update README with examples
  - [ ] Add inline documentation

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

### Example Transformation

Input: `src/utils.py`
```python
class MyClass:
    def method(self):
        pass

def my_function():
    pass
```

Output:
- `output/src/utils.py`:
  ```python
  from .utils_my_class import MyClass
  from .utils_my_function import my_function
  ```
- `output/src/utils_my_class.py`:
  ```python
  class MyClass:
      def method(self):
          pass
  ```
- `output/src/utils_my_function.py`:
  ```python
  def my_function():
      pass
  ```