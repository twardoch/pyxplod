# this_file: src/pyxplod/processors/process_dirs_method.py
"""Processing function for the 'dirs' explosion method."""

import ast
from pathlib import Path

from loguru import logger

from pyxplod.ast_utils import create_import_statement, extract_imports, find_definitions, find_module_variables
from pyxplod.file_utils import write_extracted_file
from pyxplod.processors.process_file_method import process_python_file  # Import the other processing function
from pyxplod.utils import to_snake_case


def process_python_file_dirs(input_file: Path, output_base: Path, input_root: Path) -> None:
    """Process a single Python file using the 'dirs' method.

    Creates a directory for each .py file and extracts definitions into separate files
    within that directory, with an __init__.py containing imports and module-level code.

    Special files like __init__.py, __main__.py, __version__.py are processed using
    the files method instead of creating directories.
    """
    logger.info(f"Processing (dirs): {input_file}")

    # Check if this is a special Python file (starts and ends with __)
    filename = input_file.name
    if filename.startswith("__") and filename.endswith("__.py"):
        logger.debug(f"Special file detected, using files method for: {filename}")
        process_python_file(input_file, output_base, input_root)  # Recursive call to self.process_python_file
        return

    # Calculate relative path structure
    relative_path = input_file.relative_to(input_root)
    # Create directory name from filename (without .py extension)
    dir_name = relative_path.stem
    output_dir = output_base / relative_path.parent / dir_name
    output_dir.mkdir(parents=True, exist_ok=True)

    # Read and parse the file
    try:
        content = input_file.read_text(encoding="utf-8")
        tree = ast.parse(content, filename=str(input_file))
    except SyntaxError as e:
        logger.error(f"Syntax error in {input_file}: {e}")
        return
    except Exception as e:
        logger.error(f"Error reading {input_file}: {e}")
        return

    # Extract imports, definitions, and module variables
    imports = extract_imports(tree)
    definitions = find_definitions(tree)
    module_variables = find_module_variables(tree)

    if not definitions:
        # No definitions to extract, create __init__.py with original content
        init_file = output_dir / "__init__.py"
        init_file.write_text(content, encoding="utf-8")
        logger.debug(f"No definitions found, created __init__.py with original content for: {input_file}")
        return

    # Track created files for deduplication
    existing_files: set[str] = set()

    # Process each definition
    new_imports_for_init = []

    current_remaining_body_for_init = []
    {d[0] for d in definitions}
    import_nodes = set(imports)

    for node in tree.body:
        is_definition = False
        for def_node, _def_type, _def_name in definitions:
            if node is def_node:
                is_definition = True
                def_name = _def_name

                # Generate filename without prefix for dirs method
                snake_name = to_snake_case(def_name)
                fn = f"{snake_name}.py"

                # Handle deduplication
                if fn in existing_files:
                    counter = 2
                    while f"{snake_name}_{counter}.py" in existing_files:
                        counter += 1
                    fn = f"{snake_name}_{counter}.py"
                existing_files.add(fn)

                # Write extracted file
                extracted_path = output_dir / fn
                write_extracted_file(extracted_path, imports.copy(), def_node, module_variables)

                # Create import statement for __init__.py
                import_stmt = create_import_statement(f".{fn[:-3]}", def_name)
                new_imports_for_init.append(import_stmt)
                break

        if not is_definition and node not in import_nodes:
            current_remaining_body_for_init.append(node)

    # Create __init__.py with original imports, new imports for extracted defs, and remaining code
    init_body = imports + new_imports_for_init + current_remaining_body_for_init
    init_tree = ast.Module(body=init_body, type_ignores=tree.type_ignores)

    # Write __init__.py
    init_file = output_dir / "__init__.py"
    init_file.write_text(ast.unparse(init_tree), encoding="utf-8")
    logger.info(f"Created package: {output_dir}")
    logger.debug(f"Extracted {len(definitions)} definitions from {input_file} into {output_dir}")
