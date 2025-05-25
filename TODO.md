# TODO

- [x] Implement the tool described in `README.md`
  - [x] Create PLAN.md with detailed implementation plan
  - [x] Implement CLI interface with fire for --input and --output arguments
  - [x] Implement recursive Python file discovery in input folder
  - [x] Implement AST parsing for each Python file  
  - [x] Implement extraction of class and function definitions from AST
  - [x] Implement file creation for each class/function with proper naming
  - [x] Implement AST modification to replace definitions with imports
  - [x] Implement saving modified files to output folder
  - [x] Add comprehensive logging with loguru
  - [x] Write tests for the implementation

## Completed

The `pyxplod` tool has been successfully implemented with the following features:

- CLI interface using `fire` with `--input` and `--output` arguments
- Recursive Python file discovery
- AST-based parsing and modification
- Extracts classes and functions into separate files
- Replaces definitions with relative imports
- Preserves directory structure
- Handles edge cases (syntax errors, files without definitions)
- Comprehensive test suite with 79% code coverage
- Verbose logging with `loguru` and progress bars with `rich`
