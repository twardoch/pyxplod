# TODO
# this_file: TODO.md

## ✅ COMPLETED

### Scope Resolution (2025-05-27)
- [x] Implement module-level variable detection
- [x] Include module variables in extracted files
- [x] Fix import filtering for module variables

### Code Refactoring (2025-05-27)
- [x] Split pyxplod.py into modular components
- [x] Create utils.py, ast_utils.py, file_utils.py
- [x] Create processors.py, cli.py
- [x] Update imports and dependencies

## 🚀 Sprint 1: Code Quality (HIGH PRIORITY)

### Type Safety
- [ ] Add type hints to all functions in ast_utils.py
- [ ] Add type hints to all functions in file_utils.py
- [ ] Add type hints to all functions in processors.py
- [ ] Add type hints to all functions in cli.py
- [ ] Add return type annotations everywhere
- [ ] Use proper AST node types (ast.FunctionDef, ast.ClassDef)
- [ ] Run mypy in CI pipeline

### Error Handling
- [ ] Add --skip-errors flag for continuing on syntax errors
- [ ] Implement partial file processing on AST parse failures
- [ ] Add file:line context to all error messages
- [ ] Add proper Unicode/encoding detection and handling
- [ ] Validate all user inputs with clear error messages

### Logging
- [ ] Add this_file markers to all source files
- [ ] Implement --log-level CLI option
- [ ] Add --log-file option for debugging
- [ ] Add timing information for performance analysis
- [ ] Use consistent loguru patterns

### Code Preservation
- [ ] Fix decorator preservation (@property, @staticmethod)
- [ ] Fix docstring position relative to imports
- [ ] Preserve comments between definitions
- [ ] Handle complex decorator chains properly

## 🎯 Sprint 2: Essential Features (HIGH PRIORITY)

### CLI Features
- [ ] Implement --dry-run mode
- [ ] Add .pyxplod.toml configuration file support
- [ ] Create example configuration file
- [ ] Document all configuration options

### File Filtering
- [ ] Add --exclude pattern support (glob patterns)
- [ ] Add --include pattern support
- [ ] Support .pyxplodignore file
- [ ] Add --include-private flag for _methods

### Advanced Code
- [ ] Support nested class extraction
- [ ] Handle inner functions properly
- [ ] Support async functions and decorators

## 📚 Sprint 3: Testing & Docs (MEDIUM PRIORITY)

### Testing
- [ ] Increase test coverage to 95%+
- [ ] Add edge case tests for Unicode files
- [ ] Add error condition tests
- [ ] Add property-based testing with Hypothesis
- [ ] Add integration tests with popular packages

### Documentation
- [ ] Add comprehensive docstrings to all public functions
- [ ] Create API documentation with Sphinx
- [ ] Add visual before/after examples to README
- [ ] Add troubleshooting guide
- [ ] Add FAQ section

## ⚡ Sprint 4: Performance (LOW PRIORITY)

### Optimization
- [ ] Implement parallel file processing
- [ ] Add streaming for large files
- [ ] Create incremental processing mode
- [ ] Add progress persistence

### Advanced Features
- [ ] Add --format option with Black integration
- [ ] Implement --method implode (reverse operation)
- [ ] Add --verify mode for output validation

## 📦 Sprint 5: Distribution (LOW PRIORITY)

### Packaging
- [ ] Improve package metadata
- [ ] Create standalone executables
- [ ] Add pre-commit hook support
- [ ] Consider IDE plugin development

## 🔧 Technical Debt

### Code Cleanup
- [ ] Remove unused variables and imports
- [ ] Consolidate duplicate code patterns
- [ ] Add constants for magic values
- [ ] Improve variable naming consistency

### Architecture
- [ ] Consider plugin architecture
- [ ] Abstract file I/O for testing
- [ ] Improve separation of concerns

## 📊 Next Actions (in order)

1. [ ] Add type hints to ast_utils.py
2. [ ] Add type hints to file_utils.py
3. [ ] Implement --dry-run mode
4. [ ] Add --skip-errors flag
5. [ ] Fix decorator preservation
6. [ ] Add .pyxplod.toml support
7. [ ] Increase test coverage to 95%
8. [ ] Add comprehensive docstrings
9. [ ] Implement --exclude patterns
10. [ ] Support nested classes