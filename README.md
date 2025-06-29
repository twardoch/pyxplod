# pyxplod: Python Code Exploder

## Part 1: Accessible Overview

### What is pyxplod?

`pyxplod` is a command-line tool designed to refactor Python codebases by "exploding" them. It takes Python files and automatically extracts top-level classes and functions into their own separate files. The original files are then updated to import these extracted components. This process helps in breaking down large, monolithic Python files into smaller, more manageable, and modular units.

### Who is it for?

`pyxplod` is beneficial for:

*   **Developers working on large Python projects:** It can help declutter modules and make the codebase easier to navigate and understand.
*   **Software engineers looking to refactor legacy code:** It provides an automated first step towards modularizing complex files.
*   **Teams aiming to improve code organization:** It encourages a more granular structure, potentially leading to better separation of concerns.
*   **Educators and students:** It can be used to demonstrate concepts of code modularity, imports, and project structure in Python.

### Why is it useful?

Using `pyxplod` offers several advantages:

*   **Improved Code Organization:** Breaks down large files into smaller, focused modules.
*   **Enhanced Readability:** Smaller files are generally easier to read and comprehend.
*   **Better Maintainability:** Changes to a specific class or function are isolated to its own file, reducing the risk of unintended side effects.
*   **Clearer Dependencies:** While `pyxplod` handles import management during explosion, the resulting structure can make it easier to visualize dependencies between components.
*   **Facilitates Refactoring:** Acts as an initial automated step that can simplify further refactoring efforts.

### Installation

`pyxplod` is a Python package. You can install it using `uv pip`.

1.  **From PyPI (Recommended if available):**
    ```bash
    uv pip install pyxplod
    ```
    *(Note: This assumes the package is published to PyPI. If not, use the method below.)*

2.  **From source (after cloning the repository):**
    ```bash
    git clone <repository_url>
    cd pyxplod
    uv pip install .
    ```

### How to Use

`pyxplod` is primarily a command-line tool.

#### Command-Line Interface (CLI)

The basic command structure is:

```bash
pyxplod <input_directory> <output_directory> --method <method_name> [--verbose]
```

**Arguments:**

*   `input_directory`: The path to the directory containing the Python project or files you want to explode.
*   `output_directory`: The path to the directory where `pyxplod` will save the exploded files and the modified project structure. This directory will be created if it doesn't exist.
*   `--method <method_name>`: (Required) Specifies the explosion strategy.
    *   `files`: Extracts each class/function into a new file named `original_filename_extracted_definition_name.py` within the same relative directory structure in the output path. The original file is modified to import these new files.
    *   `dirs`: For each processed `.py` file (e.g., `module.py`), this method creates a new directory (e.g., `module/`) in the output path. Extracted classes/functions are saved as individual files (e.g., `my_function.py`, `my_class.py`) within this new directory. An `__init__.py` file is generated inside this directory, containing necessary imports for the extracted components and any remaining module-level code from the original file. Special files like `__init__.py` or `__main__.py` are processed using the `files` method logic even if `dirs` is selected.
*   `--verbose`: (Optional) Enables verbose logging, providing more detailed output about the tool's operations. Useful for debugging.

**Example:**

If you have a project in `my_project/` and want to explode it into `my_project_exploded/` using the `dirs` method:

```bash
pyxplod my_project/ my_project_exploded/ --method dirs --verbose
```

#### Programmatic Usage

While primarily a CLI tool, the core functionality can be accessed programmatically by importing and calling the `main` function from the `pyxplod.cli` module.

```python
# main_script.py
from pyxplod.cli import main

if __name__ == "__main__":
    input_dir = "path/to/your/input_project"
    output_dir = "path/to/your/output_project"
    explosion_method = "files"  # or "dirs"
    verbose_mode = True # or False

    try:
        main(input_dir, output_dir, method=explosion_method, verbose=verbose_mode)
        print(f"Project exploded successfully to {output_dir}")
    except Exception as e:
        print(f"An error occurred: {e}")

```

## Part 2: Technical Details

### How the Code Works Precisely

`pyxplod` refactors Python code by parsing it into an Abstract Syntax Tree (AST) and then restructuring it based on the chosen method.

1.  **File Discovery:** The tool starts by scanning the specified `input_directory` recursively for all Python files (`.py`), ignoring common non-code directories like `__pycache__`.

2.  **AST Parsing:** Each discovered Python file is read and parsed into an AST using Python's built-in `ast` module. This tree represents the syntactic structure of the code.

3.  **Definition Identification:** The AST is traversed to identify all top-level (module-level) class definitions (`ast.ClassDef`) and function definitions (`ast.FunctionDef`).

4.  **Extraction Process (for each definition):**
    *   **Name Usage Analysis:** The AST node corresponding to the class or function definition is analyzed to determine all names (variables, functions, classes, modules) it uses. This includes names used in decorators.
    *   **Module Variable Handling:** Module-level variable assignments (e.g., `MY_CONSTANT = 10`) are identified. If an extracted definition uses any of these module-level variables, those variable assignments are also included in the new file created for the definition.
    *   **Import Filtering:** The original import statements (`ast.Import`, `ast.ImportFrom`) from the source file are analyzed. Only the imports that are actually necessary for the current definition (and any module variables it uses) are included in the new file. This ensures that extracted files are self-contained with minimal necessary imports.
    *   **New File Creation:**
        *   A new Python file is generated. Its name and location depend on the chosen `--method`.
        *   This file contains:
            1.  The filtered, necessary import statements.
            2.  Any required module-level variable assignments.
            3.  The class or function definition itself.
        *   The content is generated by unparsing the constructed AST for the new file.

5.  **Original File Modification:**
    *   The extracted class and function definitions are removed from the AST of the original file.
    *   New import statements are added to the original file's AST to import the extracted definitions from their new locations. For example, if `MyClass` was extracted to `original_module_my_class.py`, an `from .original_module_my_class import MyClass` (or similar, depending on the method) would be added.
    *   The modified AST of the original file is then unparsed back into Python code and overwrites the original file in the `output_directory`.

6.  **Processing Methods:**

    *   **`--method files`:**
        *   **File Naming:** New files are named using the pattern: `output_base_dir/relative_path_to_original/original_stem_snake_case_definition_name.py`. For example, if `src/utils.py` contains `MyHelperClass`, it might be extracted to `output/src/utils_my_helper_class.py`.
        *   **Original File:** The original file (e.g., `output/src/utils.py`) is modified to import from these newly created sibling files (e.g., `from .utils_my_helper_class import MyHelperClass`).

    *   **`--method dirs`:**
        *   **Directory Structure:** For each Python file (e.g., `my_module.py` in `src/`), a new directory is created in the output (e.g., `output/src/my_module/`).
        *   **File Naming:** Extracted definitions are saved as `.py` files within this new directory, using a snake_case version of their names (e.g., `output/src/my_module/my_function.py`, `output/src/my_module/my_class.py`).
        *   **`__init__.py` Generation:** An `__init__.py` file is created within the new directory (e.g., `output/src/my_module/__init__.py`). This `__init__.py` file will contain:
            1.  The original import statements from `my_module.py`.
            2.  New import statements to import the extracted definitions from their files within the `my_module/` directory (e.g., `from .my_function import my_function`).
            3.  Any remaining module-level code (variables, simple statements) from the original `my_module.py` that was not part of an extracted definition or an import.
        *   **Special Files:** Files like `__init__.py`, `__main__.py`, etc., are handled using the `files` method logic to avoid creating subdirectories for them (e.g., an `__init__/` directory).

7.  **Key Modules:**
    *   `pyxplod.cli`: Handles command-line argument parsing (using `fire`), logging setup (`loguru`, `rich`), and orchestrates the overall process.
    *   `pyxplod.ast_utils`: Provides utilities for working with ASTs, such as extracting imports, finding definitions, analyzing name usage within nodes, and filtering imports based on usage.
    *   `pyxplod.file_utils`: Manages file system operations like finding Python files, validating paths, generating unique filenames for extracted code (handling potential name collisions), and writing the new AST-generated Python code to files.
    *   `pyxplod.processors`: Contains the core logic for processing individual Python files. It implements the `files` and `dirs` explosion strategies, utilizing `ast_utils` and `file_utils`.
    *   `pyxplod.utils`: General utility functions (e.g., `to_snake_case`).

### Rules of Coding and Contributing

This project follows specific guidelines for coding and contributions, largely outlined in `CLAUDE.md`. Contributors are expected to familiarize themselves with it. Here's a summary:

**General Principles (from `CLAUDE.md`):**

*   **Iterative Development:** Make gradual changes. Avoid large, sweeping modifications at once.
*   **Preserve Structure:** Maintain existing code and project structure unless a change is well-justified.
*   **Clarity and Simplicity:**
    *   Use constants instead of magic numbers.
    *   Write clear, explanatory docstrings and comments. Explain **what** the code does and **why** it does it. Also, note where and how the code is used or referred to elsewhere.
    *   Modularize repeated logic into concise, single-purpose functions.
    *   Favor flat structures over deeply nested ones.
*   **Robustness:** Handle failures gracefully. Address edge cases, validate assumptions, and catch errors early.
*   **Efficiency:** Let the computer do the work; minimize unnecessary user decisions.
*   **Codebase Awareness:** Check for existing solutions within the codebase before implementing new ones. Maintain a holistic overview of the codebase.
*   **File Path Tracking:** In each source file, maintain an up-to-date `this_file:` comment near the top, indicating the file's path relative to the project root.

**Python-Specific Guidelines (from `CLAUDE.md`):**

*   **Package Management:** Use `uv pip` for managing dependencies (e.g., `uv pip install <package>`).
*   **Execution:** Use `python -m <module>` when running Python modules.
*   **Style and Formatting:**
    *   Adhere to PEP 8 (Code Layout, Naming Conventions).
    *   Follow PEP 20 (The Zen of Python) principles – prioritize readability, simplicity, and explicitness.
    *   Use type hints in their simplest form (e.g., `list`, `dict`, `str | int`).
*   **Docstrings:** Write clear, imperative docstrings as per PEP 257.
*   **Language Features:** Utilize f-strings for string formatting. Consider structural pattern matching where appropriate.
*   **Logging:** Implement `loguru`-based logging with a "verbose" mode and debug logs.
*   **CLI Scripts:** For command-line interface scripts, use `fire` for argument parsing and `rich` for enhanced terminal output. Start scripts with the shebang:
    ```python
    #!/usr/bin/env -S uv run -s
    # /// script
    # dependencies = ["PKG1", "PKG2"]
    # ///
    # this_file: path/to/current_file.py
    ```

**Development Workflow (from `CLAUDE.md`):**

1.  **Planning:**
    *   Create/Update `PLAN.md` with a detailed flat list of tasks (`[ ]` items).
    *   Identify key items and create/update `TODO.md` (`[ ]` items).
2.  **Implementation:** Implement the changes.
3.  **Tracking:** Update `PLAN.md` and `TODO.md` as you progress.
4.  **Changelog:** After each significant round of changes, update `CHANGELOG.md`.
5.  **Documentation:** Update `README.md` to reflect any user-facing changes.

**Code Quality and Testing (from `CLAUDE.md`):**

*   After making Python code changes, run the following sequence of commands to ensure code quality and correctness:
    ```bash
    fd -e py -x autoflake {}; \
    fd -e py -x pyupgrade --py311-plus {}; \
    fd -e py -x ruff check --output-format=github --fix --unsafe-fixes {}; \
    fd -e py -x ruff format --respect-gitignore --target-version py311 {}; \
    python -m pytest
    ```
    *(Ensure `fd-find` (for `fd`), `autoflake`, `pyupgrade`, `ruff`, and `pytest` are installed in your development environment.)*

**Contribution Process (General Best Practices):**

1.  **Fork the Repository:** Create your own fork of the `pyxplod` repository.
2.  **Create a Feature Branch:** Branch off `main` (or the relevant development branch) for your changes (e.g., `git checkout -b feature/my-new-feature`).
3.  **Make Changes:** Implement your feature or bug fix.
4.  **Add Tests:** Write unit tests for any new functionality or to cover bug fixes.
5.  **Run Checks:** Execute the code quality and testing script mentioned above to ensure your changes pass all checks.
6.  **Update Documentation:** If your changes affect user-facing aspects or the technical workings, update `README.md` and other relevant documentation (`PLAN.md`, `TODO.md`, `CHANGELOG.md`).
7.  **Commit Changes:** Commit your work with clear, descriptive commit messages.
8.  **Push to Your Fork:** Push your feature branch to your fork on GitHub.
9.  **Submit a Pull Request:** Open a pull request from your feature branch to the main `pyxplod` repository. Clearly describe the changes you've made and why.

By following these guidelines, we can maintain a high-quality, understandable, and collaborative codebase.
