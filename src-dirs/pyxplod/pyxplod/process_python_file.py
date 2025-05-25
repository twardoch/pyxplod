import ast
from pathlib import Path

from loguru import logger


def process_python_file(input_file: Path, output_base: Path, input_root: Path) -> None:
    """Process a single Python file, extracting definitions and creating new files."""
    logger.info(f"Processing: {input_file}")
    relative_path = input_file.relative_to(input_root)
    output_dir = output_base / relative_path.parent
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
        output_file = output_base / relative_path
        output_file.write_text(content, encoding="utf-8")
        logger.debug(f"No definitions found, copied: {input_file}")
        return
    existing_files = set()
    base_name = input_file.stem
    new_imports = []
    remaining_body = []
    for node in tree.body:
        is_definition = False
        for def_node, def_type, def_name in definitions:
            if node is def_node:
                is_definition = True
                filename = generate_filename(base_name, def_name, def_type, existing_files)
                extracted_path = output_dir / filename
                write_extracted_file(extracted_path, imports.copy(), def_node)
                import_stmt = create_import_statement(f".{filename[:-3]}", def_name)
                new_imports.append(import_stmt)
                break
        if not is_definition and node not in imports:
            remaining_body.append(node)
    modified_tree = ast.Module(body=imports + new_imports + remaining_body, type_ignores=tree.type_ignores)
    output_file = output_base / relative_path
    output_file.write_text(ast.unparse(modified_tree), encoding="utf-8")
    logger.info(f"Modified main file: {output_file}")
    logger.debug(f"Extracted {len(definitions)} definitions from {input_file}")
