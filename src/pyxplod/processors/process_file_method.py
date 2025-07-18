# this_file: src/pyxplod/processors/process_file_method.py
"""Processing function for the 'files' explosion method."""

import ast
from pathlib import Path

from loguru import logger

from pyxplod.ast_utils import create_import_statement, extract_imports, find_definitions, find_module_variables
from pyxplod.file_utils import generate_filename, write_extracted_file


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

    for node in tree.body:
        for def_node, _def_type, def_name in definitions:
            if node is def_node:
                # Generate filename for extracted definition
                filename = generate_filename(base_name, def_name, existing_files)

                # Write extracted file
                extracted_path = output_dir / filename
                write_extracted_file(extracted_path, imports.copy(), def_node, module_variables)

                # Create import statement
                import_stmt = create_import_statement(f".{filename[:-3]}", def_name)
                new_imports.append(import_stmt)
                break

    current_remaining_body = []
    definition_nodes = {d[0] for d in definitions}
    import_nodes = set(imports)

    for node in tree.body:
        if node not in definition_nodes and node not in import_nodes:
            current_remaining_body.append(node)

    modified_tree = ast.Module(body=imports + new_imports + current_remaining_body, type_ignores=tree.type_ignores)

    # Write the modified file
    output_file = output_base / relative_path
    output_file.write_text(ast.unparse(modified_tree), encoding="utf-8")
    logger.info(f"Modified main file: {output_file}")
    logger.debug(f"Extracted {len(definitions)} definitions from {input_file}")
