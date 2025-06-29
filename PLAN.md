# PLAN.md
# this_file: PLAN.md

## Project Overview

pyxplod is a Python code refactoring tool that "explodes" Python modules by extracting classes and functions into separate files. It offers two methods:
- `files`: Creates flat file structure with prefixed names
- `dirs`: Creates package directories with cleaner imports

## Current State Analysis (2025-06-29)

### ✅ Completed Features
- Core functionality for extracting classes/functions
- Two extraction methods (files/dirs)
- Module-level variable resolution
- Smart import filtering
- Basic CLI with fire
- 79% test coverage
- Modular architecture refactoring

### 🔍 Key Issues Identified

1. **Type Safety**: Minimal type hints throughout codebase
2. **Error Handling**: Basic error handling, no graceful recovery
3. **Documentation**: Missing comprehensive docstrings and API docs
4. **Features**: Missing essential features like dry-run, config files
5. **Performance**: No optimization for large codebases
6. **Code Quality**: Inconsistent logging patterns, missing validation

## Sprint 1: Code Quality & Robustness (High Priority)

### 1.1 Type System Enhancement
- [ ] Add comprehensive type hints to all functions
  - [ ] Use simple types: `list[str]`, `dict[str, Any]`, `str | None`
  - [ ] Add return type annotations
  - [ ] Use proper AST node types instead of generic `ast.AST`
  - [ ] Add type hints to test files
  - [ ] Run mypy in strict mode as part of CI

### 1.2 Error Handling & Validation
- [ ] Implement proper error recovery
  - [ ] Add `--skip-errors` flag to continue on syntax errors
  - [ ] Partial file processing when AST parsing fails
  - [ ] Better error messages with context (file:line)
  - [ ] Validate all inputs and fail early with clear messages
- [ ] Add Unicode/encoding support
  - [ ] Auto-detect file encoding
  - [ ] Support UTF-8, UTF-16, Latin-1
  - [ ] Handle encoding errors gracefully

### 1.3 Logging & Debugging
- [ ] Implement proper logging pattern per CLAUDE.md
  - [ ] Add `this_file` marker to all source files
  - [ ] Use loguru consistently with proper log levels
  - [ ] Add `--log-level` CLI option
  - [ ] Log to file option with `--log-file`
  - [ ] Add timing information for performance debugging

### 1.4 Code Element Preservation
- [ ] Fix decorator preservation
  - [ ] Maintain `@property`, `@staticmethod`, `@classmethod`
  - [ ] Handle complex decorator chains
  - [ ] Preserve decorator arguments
- [ ] Fix docstring handling
  - [ ] Preserve docstring position relative to imports
  - [ ] Handle multi-line docstrings correctly
  - [ ] Maintain docstring formatting
- [ ] Preserve comments
  - [ ] Extract comments between definitions
  - [ ] Maintain inline comments
  - [ ] Handle block comments properly

## Sprint 2: Essential Features (High Priority)

### 2.1 CLI Enhancements
- [ ] Add `--dry-run` mode
  - [ ] Show what would be changed without writing
  - [ ] Display file creation/modification summary
  - [ ] Optionally output to stdout
- [ ] Add configuration file support
  - [ ] Support `.pyxplod.toml` configuration
  - [ ] Allow project-specific settings
  - [ ] Override via CLI flags
  - [ ] Document all configuration options

### 2.2 File Filtering
- [ ] Add `--exclude` patterns
  - [ ] Support glob patterns
  - [ ] Multiple exclude patterns
  - [ ] Read from `.pyxplodignore` file
- [ ] Add `--include` patterns
  - [ ] Whitelist specific files/patterns
  - [ ] Override default Python file detection
- [ ] Add `--include-private` flag
  - [ ] Process private methods/classes (_name)
  - [ ] Process dunder methods (__name__)

### 2.3 Advanced Code Handling
- [ ] Support nested definitions
  - [ ] Extract nested classes
  - [ ] Handle inner functions
  - [ ] Maintain proper scoping
- [ ] Handle async code
  - [ ] Support async functions
  - [ ] Handle async decorators
  - [ ] Preserve async context managers

## Sprint 3: Testing & Documentation (Medium Priority)

### 3.1 Test Suite Enhancement
- [ ] Increase test coverage to 95%+
  - [ ] Add edge case tests
  - [ ] Test error conditions
  - [ ] Test Unicode handling
  - [ ] Test large files
- [ ] Add property-based testing
  - [ ] Use Hypothesis for fuzzing
  - [ ] Test with random Python code
  - [ ] Verify round-trip correctness
- [ ] Add integration tests
  - [ ] Test with popular packages (requests, flask)
  - [ ] Verify no functionality breaks
  - [ ] Performance benchmarks

### 3.2 Documentation
- [ ] Add comprehensive docstrings
  - [ ] Document all public functions
  - [ ] Add usage examples
  - [ ] Document edge cases
- [ ] Create API documentation
  - [ ] Use Sphinx for generation
  - [ ] Host on Read the Docs
  - [ ] Add architecture diagrams
- [ ] Improve README
  - [ ] Add visual examples (before/after)
  - [ ] Add troubleshooting section
  - [ ] Add FAQ section

## Sprint 4: Performance & Advanced Features (Low Priority)

### 4.1 Performance Optimization
- [ ] Implement parallel processing
  - [ ] Use multiprocessing for file processing
  - [ ] Configurable worker count
  - [ ] Progress tracking across workers
- [ ] Memory optimization
  - [ ] Stream processing for large files
  - [ ] Lazy AST evaluation
  - [ ] Garbage collection optimization
- [ ] Add incremental mode
  - [ ] Only process changed files
  - [ ] Cache processing results
  - [ ] Fast re-run support

### 4.2 Advanced Features
- [ ] Add `--format` option
  - [ ] Integrate with Black
  - [ ] Preserve original formatting option
  - [ ] Custom formatter support
- [ ] Implement reverse operation
  - [ ] `--method implode` to merge files back
  - [ ] Maintain git history
  - [ ] Handle conflicts
- [ ] Add `--verify` mode
  - [ ] Validate output correctness
  - [ ] Run basic smoke tests
  - [ ] Check import cycles

## Sprint 5: Distribution & Deployment (Low Priority)

### 5.1 Packaging Improvements
- [ ] Add better package metadata
  - [ ] Comprehensive classifiers
  - [ ] Better project description
  - [ ] Add keywords for discovery
- [ ] Create standalone executables
  - [ ] Use PyInstaller/Nuitka
  - [ ] Cross-platform binaries
  - [ ] Auto-update mechanism

### 5.2 Integration Support
- [ ] Add pre-commit hook
  - [ ] Validate code before commit
  - [ ] Auto-fix mode
  - [ ] Configuration options
- [ ] IDE plugins
  - [ ] VS Code extension
  - [ ] PyCharm plugin
  - [ ] Sublime Text package

## Technical Debt & Refactoring

### Clean Code
- [ ] Remove unused variables and imports
- [ ] Consolidate duplicate code
- [ ] Improve variable naming consistency
- [ ] Add constants for magic values

### Architecture
- [ ] Consider plugin architecture for processors
- [ ] Abstract file I/O for testability
- [ ] Improve separation of concerns
- [ ] Add facade pattern for complex operations

## Risk Mitigation

1. **Breaking Changes**: Maintain backward compatibility
2. **Performance**: Profile before optimizing
3. **Complexity**: Keep simple things simple
4. **Dependencies**: Minimize external dependencies

## Success Metrics

- Test coverage > 95%
- Zero critical bugs
- Processing speed > 1000 files/minute
- Memory usage < 100MB for typical projects
- User satisfaction (GitHub stars, issues resolved)

## Next Steps

1. Complete Sprint 1 (Code Quality)
2. Release v0.4.0 with core improvements
3. Gather user feedback
4. Prioritize Sprint 2 features based on feedback
5. Establish regular release cycle (monthly)