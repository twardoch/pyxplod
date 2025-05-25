import ast
from pathlib import Path

from loguru import logger


def write_extracted_file(output_path: Path, imports: list[ast.stmt], definition: ast.stmt) -> None:
    """Write the extracted definition to a new file with necessary imports."""
    used_names = analyze_name_usage(definition)
    filtered_imports = filter_imports_for_names(imports, used_names)
    new_module = ast.Module(body=[*filtered_imports, definition], type_ignores=[])
    code = ast.unparse(new_module)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(code, encoding="utf-8")
    logger.debug(f"Created file: {output_path} with {len(filtered_imports)} imports (filtered from {len(imports)})")
