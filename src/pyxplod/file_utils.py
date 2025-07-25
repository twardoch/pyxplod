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
    use_common_module: bool = False,
    common_elements: dict[str, set[str]] | None = None,
) -> None:
    """Write the extracted definition to a new file with necessary imports and module variables.
    
    Args:
        output_path: Path to write the extracted file
        imports: List of import statements from original file
        definition: The function/class definition to extract
        module_variables: List of (node, name) tuples for module variables
        use_common_module: Whether to import from common module
        common_elements: Dict of element names that are in common module
    """
    if module_variables is None:
        module_variables = []
    if common_elements is None:
        common_elements = {'imports': set(), 'constants': set(), 'variables': set()}

    # Analyze which names are actually used in the definition
    used_names = analyze_name_usage(definition)

    body = []
    
    # If using common module, add import from it
    if use_common_module:
        # Check what we need from common module
        needed_from_common = set()
        
        # Check for constants
        for const_name in common_elements.get('constants', set()):
            if const_name in used_names:
                needed_from_common.add(const_name)
        
        # Check for variables
        for var_name in common_elements.get('variables', set()):
            if var_name in used_names:
                needed_from_common.add(var_name)
        
        # Add common module import if we need anything from it
        if needed_from_common:
            # Create specific imports from common module
            common_import = ast.ImportFrom(
                module='.common',
                names=[ast.alias(name=name, asname=None) for name in sorted(needed_from_common)],
                level=0
            )
            body.append(common_import)
            
            # Remove imported names from used_names so we don't duplicate imports
            used_names -= needed_from_common
        
        # Also import all original imports from common if needed
        # Check if any imports are used
        imports_used = False
        for imp in imports:
            if isinstance(imp, ast.Import):
                for alias in imp.names:
                    name_in_code = alias.asname or alias.name
                    base_name = name_in_code.split(".")[0]
                    if base_name in used_names:
                        imports_used = True
                        break
            elif isinstance(imp, ast.ImportFrom):
                for alias in imp.names:
                    name_in_code = alias.asname or alias.name
                    if name_in_code in used_names:
                        imports_used = True
                        break
            if imports_used:
                break
        
        if imports_used:
            # Import * from common to get all imports
            star_import = ast.ImportFrom(
                module='.common',
                names=[ast.alias(name='*', asname=None)],
                level=0
            )
            body.insert(0, star_import)
            # Don't need individual imports anymore
            filtered_imports = []
        else:
            # No imports needed
            filtered_imports = []
    else:
        # Original behavior - include filtered imports directly
        # Find which module variables are needed by this definition
        needed_variables = []
        for var_node, var_name in module_variables:
            if var_name in used_names:
                needed_variables.append(var_node)
                # Also analyze names used in the variable assignment itself
                var_used_names = analyze_name_usage(var_node)
                used_names.update(var_used_names)
                logger.debug(f"Including module variable '{var_name}' in {output_path.name}")

        # Filter imports to include those used by both definition and needed variables
        filtered_imports = filter_imports_for_names(imports, used_names)
        body.extend(filtered_imports)
        body.extend(needed_variables)

    # Add the definition
    body.append(definition)

    # Create a new module
    new_module = ast.Module(body=body, type_ignores=[])

    # Generate Python code from AST
    code = ast.unparse(new_module)

    # Write to file with UTF-8 encoding
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(code, encoding="utf-8")
    
    if use_common_module:
        logger.debug(f"Created file: {output_path} importing from common module")
    else:
        logger.debug(f"Created file: {output_path} with {len(filtered_imports)} imports")


def find_python_files(directory: Path) -> list[Path]:
    """Recursively find all Python files in a directory."""
    python_files: list[Path] = [
        file for file in directory.rglob("*.py") if "__pycache__" not in str(file) and ".pyc" not in str(file)
    ]
    return sorted(python_files)


def write_common_module(
    output_path: Path,
    imports: list[ast.stmt],
    constants: list[tuple[ast.stmt, str]],
    variables: list[tuple[ast.stmt, str]],
) -> None:
    """Write a common module containing shared imports, constants, and variables.
    
    Args:
        output_path: Path to write the common.py file
        imports: List of import statements
        constants: List of (node, name) tuples for constants
        variables: List of (node, name) tuples for module variables
    """
    # Collect all nodes in order: imports, then constants, then variables
    body = []
    
    # Add file location comment
    file_comment = ast.Expr(value=ast.Constant(value=f"# this_file: {output_path.relative_to(output_path.parent.parent)}"))
    body.append(file_comment)
    
    # Add docstring
    docstring = ast.Expr(value=ast.Constant(value="Common imports, constants, and variables shared across split modules."))
    body.append(docstring)
    
    # Add imports
    body.extend(imports)
    
    # Add a blank line (as a comment) if we have imports
    if imports:
        body.append(ast.Expr(value=ast.Constant(value="")))
    
    # Add constants
    body.extend(node for node, _ in constants)
    
    # Add a blank line if we have constants and variables
    if constants and variables:
        body.append(ast.Expr(value=ast.Constant(value="")))
    
    # Add variables
    body.extend(node for node, _ in variables)
    
    # Create module
    module = ast.Module(body=body, type_ignores=[])
    
    # Generate code
    code = ast.unparse(module)
    
    # Clean up the code (remove expressions that are just strings)
    lines = code.split('\n')
    cleaned_lines = []
    for line in lines:
        # Skip lines that are just string expressions (our spacing hack)
        if line.strip() in ('""', "''"):
            cleaned_lines.append("")  # Empty line
        elif line.strip().startswith("'# this_file:"):
            # Fix the file comment
            cleaned_lines.append(line.strip()[1:-1])  # Remove quotes
        elif line.strip().startswith('"Common imports'):
            # Fix the docstring
            cleaned_lines.append('"""Common imports, constants, and variables shared across split modules."""')
        else:
            cleaned_lines.append(line)
    
    code = '\n'.join(cleaned_lines)
    
    # Write to file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(code, encoding="utf-8")
    logger.debug(f"Created common module: {output_path} with {len(imports)} imports, {len(constants)} constants, {len(variables)} variables")


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
