#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["fire", "loguru", "rich"]
# ///
# this_file: src/pyxplod/pyxplod.py

"""pyxplod: Python code exploder - extracts classes and functions into separate files.

This tool takes a Python project and "explodes" it by extracting each class and function
definition into its own file, replacing the original definitions with imports.
"""

import ast
import re
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import fire
from loguru import logger
from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn

console = Console()


def to_snake_case(name: str) -> str:
    """Convert a name to snake_case format.

    Handles CamelCase, pascalCase, and already snake_case names.
    """
    # Insert underscores before uppercase letters that follow lowercase letters
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    # Insert underscores before uppercase letters that follow lowercase or uppercase letters
    s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
    # Convert to lowercase
    return s2.lower()


def extract_imports(tree: ast.AST) -> list[ast.stmt]:
    """Extract all import statements from an AST.

    Returns a list of Import and ImportFrom nodes at module level only.
    """
    imports = []
    for node in tree.body:
        if isinstance(node, ast.Import | ast.ImportFrom):
            imports.append(node)
    return imports


def find_definitions(tree: ast.AST) -> list[tuple[ast.stmt, str, str]]:
    """Find all class and function definitions at module level.

    Returns list of tuples: (node, type, name) where type is 'class' or 'function'.
    """
    definitions = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            definitions.append((node, "class", node.name))
        elif isinstance(node, ast.FunctionDef):
            definitions.append((node, "function", node.name))
    return definitions


def generate_filename(base_name: str, def_name: str, def_type: str, existing_files: set) -> str:
    """Generate a unique filename for the extracted definition.

    Handles deduplication by appending numbers if necessary.
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


def create_import_statement(module_path: str, name: str) -> ast.ImportFrom:
    """Create an import statement for the extracted definition."""
    return ast.ImportFrom(
        module=module_path,
        names=[ast.alias(name=name, asname=None)],
        level=0,  # Absolute import from module
    )


def write_extracted_file(output_path: Path, imports: list[ast.stmt], definition: ast.stmt) -> None:
    """Write the extracted definition to a new file with necessary imports."""
    # Create a new module with imports and the definition
    new_module = ast.Module(body=[*imports, definition], type_ignores=[])

    # Generate Python code from AST
    code = ast.unparse(new_module)

    # Write to file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(code)
    logger.debug(f"Created file: {output_path}")


def process_python_file(input_file: Path, output_base: Path, input_root: Path) -> None:
    """Process a single Python file, extracting definitions and creating new files."""
    logger.info(f"Processing: {input_file}")

    # Calculate relative path structure
    relative_path = input_file.relative_to(input_root)
    output_dir = output_base / relative_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # Read and parse the file
    try:
        content = input_file.read_text()
        tree = ast.parse(content, filename=str(input_file))
    except SyntaxError as e:
        logger.error(f"Syntax error in {input_file}: {e}")
        return
    except Exception as e:
        logger.error(f"Error reading {input_file}: {e}")
        return

    # Extract imports and definitions
    imports = extract_imports(tree)
    definitions = find_definitions(tree)

    if not definitions:
        # No definitions to extract, just copy the file
        output_file = output_base / relative_path
        output_file.write_text(content)
        logger.debug(f"No definitions found, copied: {input_file}")
        return

    # Track created files for deduplication
    existing_files = set()
    base_name = input_file.stem

    # Process each definition
    new_imports = []
    remaining_body = []

    for node in tree.body:
        is_definition = False

        for def_node, def_type, def_name in definitions:
            if node is def_node:
                is_definition = True

                # Generate filename for extracted definition
                filename = generate_filename(base_name, def_name, def_type, existing_files)

                # Write extracted file
                extracted_path = output_dir / filename
                write_extracted_file(extracted_path, imports.copy(), def_node)

                # Create import statement
                import_stmt = create_import_statement(f".{filename[:-3]}", def_name)
                new_imports.append(import_stmt)
                break

        if not is_definition and node not in imports:
            remaining_body.append(node)

    # Create the modified main file
    modified_tree = ast.Module(body=imports + new_imports + remaining_body, type_ignores=tree.type_ignores)

    # Write the modified file
    output_file = output_base / relative_path
    output_file.write_text(ast.unparse(modified_tree))
    logger.info(f"Modified main file: {output_file}")
    logger.debug(f"Extracted {len(definitions)} definitions from {input_file}")


def find_python_files(directory: Path) -> list[Path]:
    """Recursively find all Python files in a directory."""
    python_files = []
    for file in directory.rglob("*.py"):
        # Skip __pycache__ and other Python metadata
        if "__pycache__" not in str(file) and ".pyc" not in str(file):
            python_files.append(file)
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


def main(input: str, output: str, verbose: bool = False) -> None:
    """Explode a Python project by extracting classes and functions into separate files.

    Args:
        input: Path to the input directory containing Python files
        output: Path to the output directory where exploded files will be created
        verbose: Enable verbose logging for debugging
    """
    # Configure logging
    if verbose:
        logger.remove()
        logger.add(console.print, format="{time:HH:mm:ss} | {level} | {message}", level="DEBUG")
    else:
        logger.remove()
        logger.add(console.print, format="{message}", level="INFO")

    # Convert to Path objects
    input_path = Path(input).resolve()
    output_path = Path(output).resolve()

    # Validate paths
    if not validate_paths(input_path, output_path):
        return

    # Find all Python files
    python_files = find_python_files(input_path)

    if not python_files:
        logger.warning(f"No Python files found in {input_path}")
        return

    logger.info(f"Found {len(python_files)} Python files to process")

    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)

    # Process each file with progress bar
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        task = progress.add_task("Processing files...", total=len(python_files))

        for py_file in python_files:
            try:
                process_python_file(py_file, output_path, input_path)
                progress.update(task, advance=1)
            except Exception as e:
                logger.error(f"Failed to process {py_file}: {e}")
                if verbose:
                    logger.exception("Detailed error:")

    logger.info(f"✨ Successfully exploded {len(python_files)} files to {output_path}")


if __name__ == "__main__":
    fire.Fire(main)
