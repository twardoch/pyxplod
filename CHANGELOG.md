# CHANGELOG

## [Unreleased]

### Changed
- Updated project documentation and planning files
- Reorganized TODO.md with sprint-based task organization  
- Refined PLAN.md with clearer phase priorities and updated status
- Enhanced README.md with more comprehensive examples and professional formatting

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