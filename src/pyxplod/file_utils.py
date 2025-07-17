# this_file: src/pyxplod/file_utils.py
"""File system and path related utility functions for pyxplod."""

import ast
from pathlib import Path

# For Python 3.9+, list, set, tuple are standard types for hinting.
from loguru import logger

from pyxplod.ast_utils import analyze_name_usage, filter_imports_for_names
from pyxplod.utils import to_snake_case


def generate_filename(base_name: str, def_name: str, existing_files: set) -> str:  # def_type removed
    """Generate a unique filename for the extracted definition.

    Handles deduplication by appending numbers if necessary.
    The def_type argument was previously unused.
    """
    snake_name = to_snake_case(def_name)
    filename = f"{base_name}_{snake_name}.py"

    # Handle deduplication
    if filename in existing_files:
        counter = 2
        while f"{base_name}_{snake_name}_{counter}.py" in existing_files:
            counter += 1
        filename = f"{base_name}_{snake_name}_{counter}.py"

    existing_files.add(filename)
    return filename


def write_extracted_file(
    output_path: Path,
    imports: list[ast.stmt],
    definition: ast.stmt,
    module_variables: list[tuple[ast.stmt, str]] | None = None,
) -> None:
    """Write the extracted definition to a new file with necessary imports and module variables."""
    if module_variables is None:
        module_variables = []

    # Analyze which names are actually used in the definition
    used_names = analyze_name_usage(definition)

    # Find which module variables are needed by this definition
    needed_variables = []
    # variable_names = set() # This variable was unused
    for var_node, var_name in module_variables:
        if var_name in used_names:
            needed_variables.append(var_node)
            # variable_names.add(var_name) # This variable was unused
            # Also analyze names used in the variable assignment itself
            var_used_names = analyze_name_usage(var_node)
            used_names.update(var_used_names)
            logger.debug(f"Including module variable '{var_name}' in {output_path.name}")

    # Filter imports to include those used by both definition and needed variables
    filtered_imports = filter_imports_for_names(imports, used_names)

    # Create a new module with filtered imports, needed variables, and the definition
    # Order: imports first, then module variables, then definition
    new_module = ast.Module(body=[*filtered_imports, *needed_variables, definition], type_ignores=[])

    # Generate Python code from AST
    code = ast.unparse(new_module)

    # Write to file with UTF-8 encoding
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(code, encoding="utf-8")
    logger.debug(f"Created file: {output_path} with {len(filtered_imports)} imports, {len(needed_variables)} variables")


def find_python_files(directory: Path) -> list[Path]:
    """Recursively find all Python files in a directory."""
    python_files: list[Path] = [
        file for file in directory.rglob("*.py") if "__pycache__" not in str(file) and ".pyc" not in str(file)
    ]
    return sorted(python_files)


def validate_paths(input_path: Path, output_path: Path) -> bool:
    """Validate input and output paths."""
    if not input_path.exists():
        logger.error(f"Input path does not exist: {input_path}")
        return False

    if not input_path.is_dir():
        logger.error(f"Input path is not a directory: {input_path}")
        return False

    if output_path.exists() and not output_path.is_dir():
        logger.error(f"Output path exists but is not a directory: {output_path}")
        return False

    return True
