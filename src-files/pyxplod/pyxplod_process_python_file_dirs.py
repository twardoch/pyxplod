import ast
from pathlib import Path

from loguru import logger


def process_python_file_dirs(input_file: Path, output_base: Path, input_root: Path) -> None:
    """Process a single Python file using the 'dirs' method.

    Creates a directory for each .py file and extracts definitions into separate files
    within that directory, with an __init__.py containing imports and module-level code.
    """
    logger.info(f"Processing (dirs): {input_file}")
    relative_path = input_file.relative_to(input_root)
    dir_name = relative_path.stem
    output_dir = output_base / relative_path.parent / dir_name
    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        content = input_file.read_text(encoding="utf-8")
        tree = ast.parse(content, filename=str(input_file))
    except SyntaxError as e:
        logger.error(f"Syntax error in {input_file}: {e}")
        return
    except Exception as e:
        logger.error(f"Error reading {input_file}: {e}")
        return
    imports = extract_imports(tree)
    definitions = find_definitions(tree)
    if not definitions:
        init_file = output_dir / "__init__.py"
        init_file.write_text(content, encoding="utf-8")
        logger.debug(f"No definitions found, created __init__.py: {input_file}")
        return
    existing_files = set()
    new_imports = []
    remaining_body = []
    for node in tree.body:
        is_definition = False
        for def_node, _def_type, def_name in definitions:
            if node is def_node:
                is_definition = True
                snake_name = to_snake_case(def_name)
                filename = f"{snake_name}.py"
                if filename in existing_files:
                    counter = 2
                    while f"{snake_name}_{counter}.py" in existing_files:
                        counter += 1
                    filename = f"{snake_name}_{counter}.py"
                existing_files.add(filename)
                extracted_path = output_dir / filename
                write_extracted_file(extracted_path, imports.copy(), def_node)
                import_stmt = create_import_statement(f".{filename[:-3]}", def_name)
                new_imports.append(import_stmt)
                break
        if not is_definition and node not in imports:
            remaining_body.append(node)
    init_tree = ast.Module(body=imports + new_imports + remaining_body, type_ignores=tree.type_ignores)
    init_file = output_dir / "__init__.py"
    init_file.write_text(ast.unparse(init_tree), encoding="utf-8")
    logger.info(f"Created package: {output_dir}")
    logger.debug(f"Extracted {len(definitions)} definitions from {input_file}")
