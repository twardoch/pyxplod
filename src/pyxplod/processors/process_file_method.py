# this_file: src/pyxplod/processors/process_file_method.py
"""Processing function for the 'files' explosion method."""

import ast
from pathlib import Path

from loguru import logger

from pyxplod.ast_utils import create_import_statement, extract_imports, find_definitions, find_module_variables, find_module_constants, find_all_module_level_elements
from pyxplod.file_utils import generate_filename, write_extracted_file, write_common_module


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

    # Extract all module-level elements
    elements = find_all_module_level_elements(tree)
    imports = elements['imports']
    definitions = elements['definitions']
    constants = elements['constants']
    variables = elements['variables']

    if not definitions:
        # No definitions to extract, just copy the file
        output_file = output_base / relative_path
        output_file.write_text(content, encoding="utf-8")
        logger.debug(f"No definitions found, copied: {input_file}")
        return

    # Track created files for deduplication
    existing_files: set[str] = set()
    base_name = input_file.stem

    # Check if we need a common module (if we have imports, constants, or variables)
    need_common_module = bool(imports or constants or variables)
    common_module_name = ".common"  # Default value
    
    # Create common module if needed
    common_elements = {
        'imports': {imp for imp in imports},  # Store import nodes for reference
        'constants': {name for _, name in constants},
        'variables': {name for _, name in variables}
    }
    
    if need_common_module:
        common_path = output_dir / "common.py"
        # Check if common.py already exists
        if common_path.exists():
            logger.warning(f"common.py already exists in {output_dir}, using alternative name")
            common_path = output_dir / f"{base_name}_common.py"
            # Update import module name
            common_module_name = f".{base_name}_common"
            
        write_common_module(common_path, imports, constants, variables)
        logger.info(f"Created common module: {common_path}")

    # Process each definition
    new_imports = []

    for node in tree.body:
        for def_node, _def_type, def_name in definitions:
            if node is def_node:
                # Generate filename for extracted definition
                filename = generate_filename(base_name, def_name, existing_files)

                # Write extracted file
                extracted_path = output_dir / filename
                write_extracted_file(
                    extracted_path, 
                    imports.copy(), 
                    def_node, 
                    variables,  # Pass all variables, filtering happens inside
                    use_common_module=need_common_module,
                    common_elements=common_elements
                )

                # Create import statement
                import_stmt = create_import_statement(f".{filename[:-3]}", def_name)
                new_imports.append(import_stmt)
                break

    # For the main file, keep only non-definition, non-common elements
    current_remaining_body = []
    definition_nodes = {d[0] for d in definitions}
    constant_nodes = {c[0] for c in constants}
    variable_nodes = {v[0] for v in variables}
    import_nodes = set(imports)
    
    # If we have a common module, import from it
    if need_common_module:
        # Import * from common to get all imports, constants, and variables
        common_import = ast.ImportFrom(
            module=common_module_name[1:],  # Remove the leading dot for relative import
            names=[ast.alias(name='*', asname=None)],
            level=1  # Relative import
        )
        current_remaining_body.append(common_import)

    for node in tree.body:
        # Skip imports, definitions, constants, and variables (they're in common or extracted files)
        if (node not in definition_nodes and 
            node not in import_nodes and 
            node not in constant_nodes and 
            node not in variable_nodes):
            current_remaining_body.append(node)

    # Build the modified main file
    if need_common_module:
        # Just the common import, new imports for definitions, and remaining body
        modified_tree = ast.Module(body=new_imports + current_remaining_body, type_ignores=tree.type_ignores)
    else:
        # Original behavior when no common module is needed
        modified_tree = ast.Module(body=imports + new_imports + current_remaining_body, type_ignores=tree.type_ignores)

    # Write the modified file
    output_file = output_base / relative_path
    output_file.write_text(ast.unparse(modified_tree), encoding="utf-8")
    logger.info(f"Modified main file: {output_file}")
    logger.debug(f"Extracted {len(definitions)} definitions from {input_file}")
