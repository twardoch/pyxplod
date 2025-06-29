# CHANGELOG

## [Unreleased]

### Added
- Implemented scope resolution for module-level variables in both `files` and `dirs` methods (2025-05-27)
  - Added `find_module_variables()` function to detect module-level assignments
  - Enhanced `write_extracted_file()` to include required module variables in extracted files
  - Module variables like `console = Console()` are now properly included in extracted files
  - Improved import filtering to include imports needed by module variables

### Changed
- Updated `ast_utils.py` with multiple improvements for better module variable handling (2025-05-28)
- Enhanced `file_utils.py` for improved file processing (2025-05-28)
- Updated project documentation and planning files
- Reorganized TODO.md with sprint-based task organization  
- Refined PLAN.md with clearer phase priorities and updated status
- Enhanced README.md with more comprehensive examples and professional formatting

### Refactored
- **Core Module Restructuring** (2025-05-27): The main `pyxplod.py` script has been significantly refactored into a more modular architecture to improve maintainability, readability, and testability.
  - Moved utility functions (e.g., `to_snake_case`) to `src/pyxplod/utils.py`.
  - Consolidated all AST (Abstract Syntax Tree) related functions into `src/pyxplod/ast_utils.py`.
  - Grouped file system operations, path validation, and filename generation logic into `src/pyxplod/file_utils.py`.
  - Centralized the core processing logic for both `files` and `dirs` methods (`process_python_file`, `process_python_file_dirs`) into `src/pyxplod/processors.py`.
  - Migrated the command-line interface logic, including the `main` function and `fire` integration, to `src/pyxplod/cli.py`.
  - The original `src/pyxplod/pyxplod.py` now serves as a thin entry point, re-exporting `main` from `cli.py`.
  - Updated `__init__.py` and `__main__.py` to reflect new module structure and `main` function location.
  - Ensured all internal imports and dependencies are correctly resolved across the new modules.

### Documentation
- Improved task tracking and project roadmap visibility
- Better organized development priorities by sprint cycles
- Added more detailed technical specifications for remaining features

## [0.3.0] - 2025-05-25

### Added
- Import optimization: Only include imports that are actually used in extracted files
- New `analyze_name_usage()` function to detect which names are referenced in code
- New `filter_imports_for_names()` function to filter imports based on usage analysis
- Improved decorator handling in import analysis
- Better handling of attribute imports (e.g., `os.path`)

### Fixed
- Fixed import duplication bug where all imports were copied to every extracted file
- Reduced extracted file sizes by 30-50% through smart import filtering

### Changed
- Enhanced verbose logging to show import filtering statistics
- Improved code documentation with detailed docstrings

## [0.2.0] - 2025-05-25

### Added
- New `--method dirs` option for alternative explosion strategy
- Creates package directories instead of flat file structure
- Generates `__init__.py` files that maintain API compatibility
- Simpler file naming without prefix in dirs method
- Tests for the new dirs method functionality

### Changed
- Default behavior now explicitly uses `--method files`
- Updated documentation to explain both methods

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