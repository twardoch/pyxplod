# PLAN: Splitting `src/pyxplod/processors.py`

## Goal
Split the `process_python_file` and `process_python_file_dirs` functions from `src/pyxplod/processors.py` into separate files to improve modularity and maintainability.

## Reasoning
- `src/pyxplod/processors.py` is one of the largest code files (9 KB).
- It contains two distinct processing functions (`process_python_file` and `process_python_file_dirs`) that represent different explosion methods.
- Separating these functions into their own files will make the codebase more organized, easier to navigate, and reduce the cognitive load when working on specific processing logic.
- This aligns with the project's `CLAUDE.md` guidelines: "Modularize repeated logic into concise, single-purpose functions" and "Favor flat over nested structures."

## Detailed Steps

1.  **Create a new directory:**
    *   Create a new directory `src/pyxplod/processors/` to house the new files.

2.  **Create `src/pyxplod/processors/process_file_method.py`:**
    *   Move the `process_python_file` function (including its docstring and all necessary imports) from `src/pyxplod/processors.py` to this new file.
    *   Ensure all imports required by `process_python_file` are present in `src/pyxplod/processors/process_file_method.py`. These include `ast`, `Path`, `logger`, `create_import_statement`, `extract_imports`, `find_definitions`, `find_module_variables`, `generate_filename`, `write_extracted_file`.

3.  **Create `src/pyxplod/processors/process_dirs_method.py`:**
    *   Move the `process_python_file_dirs` function (including its docstring and all necessary imports) from `src/pyxplod/processors.py` to this new file.
    *   Ensure all imports required by `process_python_file_dirs` are present in `src/pyxplod/processors/process_dirs_method.py`. These include `ast`, `Path`, `logger`, `create_import_statement`, `extract_imports`, `find_definitions`, `find_module_variables`, `to_snake_case`, `write_extracted_file`, and a relative import for `process_python_file` (since `process_python_file_dirs` calls it).

4.  **Update `src/pyxplod/processors.py`:**
    *   Remove the `process_python_file` and `process_python_file_dirs` function definitions from this file.
    *   Add imports to `src/pyxplod/processors.py` to re-export these functions from their new locations.
        *   `from .processors.process_file_method import process_python_file`
        *   `from .processors.process_dirs_method import process_python_file_dirs`
    *   Update the `__all__` variable in `src/pyxplod/processors.py` if it exists, to include the re-exported functions.

5.  **Update `src/pyxplod/cli.py`:**
    *   Modify the imports in `src/pyxplod/cli.py` to import `process_python_file` and `process_python_file_dirs` from `pyxplod.processors` (which will now re-export them).
        *   `from pyxplod.processors import process_python_file, process_python_file_dirs` (This import should remain the same, as `pyxplod.processors` will now act as a facade).

6.  **Run Tests:**
    *   Execute the project's test suite (`uvx hatch test` or `python -m pytest tests/`) to ensure that the refactoring has not introduced any regressions and all functionality remains intact.

7.  **Run Linting and Formatting:**
    *   Execute the project's linting and formatting commands (`fd -e py -x autoflake {}; fd -e py -x pyupgrade --py311-plus {}; fd -e py -x ruff check --output-format=github --fix --unsafe-fixes {}; fd -e py -x ruff format --respect-gitignore --target-version py311 {};`) to ensure code quality and adherence to style guidelines.

## Verification
- All existing tests pass.
- The `pyxplod` CLI tool functions correctly for both `--method files` and `--method dirs`.
- The file structure is as expected.
- No new linting or formatting issues are introduced.
