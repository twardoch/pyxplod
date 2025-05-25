# TODO

## Sprint 1

- [x] The `dirs` method has a problem. 

```
.
├── AGENT.md
├── CHANGELOG.md
├── CLAUDE.md
├── dist
├── LICENSE
├── LLM.txt
├── package.toml
├── PLAN.md
├── pyproject.toml
├── README.md
├── src
│   └── pyxplod
│       ├── __init__.py
│       ├── __main__.py
│       ├── __pycache__
│       │   ├── __init__.cpython-312.pyc
│       │   ├── __main__.cpython-312.pyc
│       │   ├── __version__.cpython-312.pyc
│       │   └── pyxplod.cpython-312.pyc
│       ├── __version__.py
│       └── pyxplod.py
├── src-dirs
│   └── pyxplod
│       ├── __init__
│       │   └── __init__.py
│       ├── __main__
│       │   └── __init__.py
│       ├── __version__
│       │   └── __init__.py
│       └── pyxplod
│           ├── __init__.py
│           ├── analyze_name_usage.py
│           ├── create_import_statement.py
│           ├── extract_imports.py
│           ├── filter_imports_for_names.py
│           ├── find_definitions.py
│           ├── find_python_files.py
│           ├── generate_filename.py
│           ├── main.py
│           ├── process_python_file_dirs.py
│           ├── process_python_file.py
│           ├── to_snake_case.py
│           ├── validate_paths.py
│           └── write_extracted_file.py
├── src-files
│   └── pyxplod
│       ├── __init__.py
│       ├── __main__.py
│       ├── __pycache__
│       │   ├── __init__.cpython-312.pyc
│       │   ├── __main__.cpython-312.pyc
│       │   ├── __version__.cpython-312.pyc
│       │   ├── pyxplod_analyze_name_usage.cpython-312.pyc
│       │   ├── pyxplod_create_import_statement.cpython-312.pyc
│       │   ├── pyxplod_extract_imports.cpython-312.pyc
│       │   ├── pyxplod_filter_imports_for_names.cpython-312.pyc
│       │   ├── pyxplod_find_definitions.cpython-312.pyc
│       │   ├── pyxplod_find_python_files.cpython-312.pyc
│       │   ├── pyxplod_generate_filename.cpython-312.pyc
│       │   ├── pyxplod_main.cpython-312.pyc
│       │   ├── pyxplod_process_python_file_dirs.cpython-312.pyc
│       │   ├── pyxplod_process_python_file.cpython-312.pyc
│       │   ├── pyxplod_to_snake_case.cpython-312.pyc
│       │   ├── pyxplod_validate_paths.cpython-312.pyc
│       │   ├── pyxplod_write_extracted_file.cpython-312.pyc
│       │   └── pyxplod.cpython-312.pyc
│       ├── __version__.py
│       ├── pyxplod_analyze_name_usage.py
│       ├── pyxplod_create_import_statement.py
│       ├── pyxplod_extract_imports.py
│       ├── pyxplod_filter_imports_for_names.py
│       ├── pyxplod_find_definitions.py
│       ├── pyxplod_find_python_files.py
│       ├── pyxplod_generate_filename.py
│       ├── pyxplod_main.py
│       ├── pyxplod_process_python_file_dirs.py
│       ├── pyxplod_process_python_file.py
│       ├── pyxplod_to_snake_case.py
│       ├── pyxplod_validate_paths.py
│       ├── pyxplod_write_extracted_file.py
│       └── pyxplod.py
├── test_unicode.py
├── tests
│   ├── __pycache__
│   │   ├── test_package.cpython-312-pytest-8.3.5.pyc
│   │   └── test_pyxplod.cpython-312-pytest-8.3.5.pyc
│   ├── test_package.py
│   └── test_pyxplod.py
└── TODO.md

16 directories, 74 files
```

`src-dirs` and `src-files` are outputs of the `dirs` and `files` methods, respectively, from the `src` folder. 

And these: 

```
├── src-dirs
│   └── pyxplod
│       ├── __init__
│       │   └── __init__.py
│       ├── __main__
│       │   └── __init__.py
│       ├── __version__
│       │   └── __init__.py
```

must be done using the `files` method even with `dirs`. That is, the __SOMETHING__.py files should always be processed using the `files` method even if the `dirs` method is used. 



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
- [ ] **Refactor monolithic pyxplod.py** (currently 450+ lines)
  - [ ] Extract `ast_utils.py` - AST manipulation and analysis functions
  - [ ] Extract `file_utils.py` - File discovery, I/O, and path operations
  - [ ] Extract `processors.py` - Method implementation logic (files/dirs)
  - [ ] Extract `cli.py` - Command line interface and argument parsing

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

