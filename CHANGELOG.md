# CHANGELOG

## [0.1.0] - 2025-05-25

### Added
- Initial implementation of `pyxplod` tool
- CLI interface with `--input`, `--output`, and `--verbose` arguments using `fire`
- Recursive Python file discovery in input directories
- AST-based parsing and modification of Python files
- Extraction of class and function definitions into separate files
- Automatic conversion to snake_case for generated filenames
- Filename deduplication to avoid conflicts
- Replacement of definitions with relative imports
- Preservation of directory structure in output
- Module-level imports preserved in extracted files
- Error handling for syntax errors and invalid files
- Comprehensive logging with `loguru`
- Progress bar display with `rich`
- Test suite with 79% code coverage
- Support for Python 3.10+

### Features
- Deterministically "explodes" Python projects into smaller files
- Each class and function gets its own file
- Original file structure is maintained with imports
- Handles edge cases gracefully (empty files, syntax errors, etc.)

### Technical Details
- Uses Python's `ast` module for accurate parsing and code generation
- Implements proper relative imports for split files
- Maintains Python syntax validity in all generated files