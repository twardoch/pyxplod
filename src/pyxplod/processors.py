# this_file: src/pyxplod/processors.py
"""Core processing functions for exploding Python files."""

import ast
from pathlib import Path

# For Python 3.9+, list, set are standard types for hinting.
from loguru import logger

from pyxplod.ast_utils import create_import_statement, extract_imports, find_definitions, find_module_variables
from pyxplod.file_utils import generate_filename, write_extracted_file
from pyxplod.utils import to_snake_case


def process_python_file(input_file: Path, output_base: Path, input_root: Path) -> None:
    """Process a single Python file, extracting definitions and creating new files."""
    logger.info(f"Processing: {input_file}")

    # Calculate relative path structure
    relative_path = input_file.relative_to(input_root)
    output_dir = output_base / relative_path.parent
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
        # No definitions to extract, just copy the file
        output_file = output_base / relative_path
        output_file.write_text(content, encoding="utf-8")
        logger.debug(f"No definitions found, copied: {input_file}")
        return

    # Track created files for deduplication
    existing_files: set[str] = set()
    base_name = input_file.stem

    # Process each definition
    new_imports = []
    # remaining_body = [] # This list was unused

    for node in tree.body:
        is_definition = False

        for def_node, def_type, def_name in definitions: # def_type is part of the tuple from find_definitions
            if node is def_node:
                is_definition = True

                # Generate filename for extracted definition
                filename = generate_filename(base_name, def_name, existing_files) # def_type was correctly removed here

                # Write extracted file
                extracted_path = output_dir / filename
                write_extracted_file(extracted_path, imports.copy(), def_node, module_variables)

                # Create import statement
                import_stmt = create_import_statement(f".{filename[:-3]}", def_name)
                new_imports.append(import_stmt)
                break

        # The original logic for populating 'remaining_body' here was superseded by 'current_remaining_body' later.
        # if (
        #     not is_definition and node not in imports and node not in module_variables
        # ):
        #     remaining_body.append(node) # This remaining_body is not used.

    # Create the modified main file
    # We keep module variables that were not part of any extracted definition in the main file.
    # Filter module_variables to keep only those not extracted.
    # This logic might need refinement if module variables are expected to be moved or duplicated.
    # For now, they stay if not used by an extracted definition.
    # However, the current write_extracted_file copies all module_variables if they are used.
    # A simpler approach for remaining_body is to ensure it doesn't include
    # any definition nodes or original import nodes.

    current_remaining_body = []
    definition_nodes = {d[0] for d in definitions}
    import_nodes = set(imports)
    # module_variable_nodes = {mv[0] for mv in module_variables}
    # Module variables are already handled by write_extracted_file

    for node in tree.body:
        if node not in definition_nodes and node not in import_nodes:
            current_remaining_body.append(node)

    modified_tree = ast.Module(body=imports + new_imports + current_remaining_body, type_ignores=tree.type_ignores)

    # Write the modified file
    output_file = output_base / relative_path
    output_file.write_text(ast.unparse(modified_tree), encoding="utf-8")
    logger.info(f"Modified main file: {output_file}")
    logger.debug(f"Extracted {len(definitions)} definitions from {input_file}")


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

    for node in tree.body:  # Iterate to build remaining body for __init__.py
        is_definition = False
        for def_node, _def_type, _def_name in definitions:
            if node is def_node:  # This is a definition node
                is_definition = True
                def_name = _def_name  # get the actual name

                # Generate filename without prefix for dirs method
                snake_name = to_snake_case(def_name)
                fn = f"{snake_name}.py"  # Use fn to avoid conflict with outer filename

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
                break  # Found the definition, move to next node in tree.body

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
