# this_file: src/pyxplod/ast_utils.py
"""AST (Abstract Syntax Tree) related utility functions for pyxplod."""

import ast

# For Python 3.9+, list, set, tuple are standard types for hinting.
# No need to import List, Set, Tuple from typing unless for older versions or specific generic aliasing.


def extract_imports(tree: ast.AST) -> list[ast.stmt]:
    """Extract all import statements from an AST.

    Returns a list of Import and ImportFrom nodes at module level only.
    """
    imports = []
    for node in tree.body:
        if isinstance(node, ast.Import | ast.ImportFrom):
            imports.append(node)
    return imports


def analyze_name_usage(node: ast.AST) -> set[str]:
    """Analyze which names are used in an AST node.

    Returns a set of all names referenced in the node, including decorators.
    """
    names: set[str] = set()

    class NameCollector(ast.NodeVisitor):
        def visit_Name(self, node: ast.Name) -> None:  # noqa: N802
            names.add(node.id)
            self.generic_visit(node)

        def visit_Attribute(self, node: ast.Attribute) -> None:  # noqa: N802
            # For attributes like os.path, we want 'os'
            if isinstance(node.value, ast.Name):
                names.add(node.value.id)
            self.generic_visit(node)

    # First check for decorators on the node itself
    if hasattr(node, "decorator_list"):
        for decorator in node.decorator_list:  # type: ignore
            # Handle simple decorators like @my_decorator
            if isinstance(decorator, ast.Name):
                names.add(decorator.id)
            # Handle attribute decorators like @module.decorator
            elif isinstance(decorator, ast.Attribute) and isinstance(decorator.value, ast.Name):
                names.add(decorator.value.id)
            # For complex decorators, visit them
            NameCollector().visit(decorator)

    # Then collect names from the rest of the node
    NameCollector().visit(node)
    return names


def filter_imports_for_names(imports: list[ast.stmt], used_names: set[str]) -> list[ast.stmt]:
    """Filter imports to only include those that are used.

    Args:
        imports: List of import statements
        used_names: Set of names used in the code

    Returns:
        List of imports that are actually used
    """
    needed_imports = []

    for imp in imports:
        if isinstance(imp, ast.Import):
            # For 'import x, y, z', check each name
            needed_aliases = []
            for alias in imp.names:
                # The name used in code is either the alias or the module name
                name_in_code = alias.asname or alias.name
                # For module.submodule, we check the first part
                base_name = name_in_code.split(".")[0]
                if base_name in used_names:
                    needed_aliases.append(alias)

            if needed_aliases:
                # Create a new import with only needed names
                new_import = ast.Import(names=needed_aliases)
                ast.copy_location(new_import, imp)
                needed_imports.append(new_import)

        elif isinstance(imp, ast.ImportFrom):
            # For 'from x import y, z', check each imported name
            needed_aliases = []
            for alias in imp.names:
                name_in_code = alias.asname if alias.asname else alias.name
                if name_in_code in used_names:
                    needed_aliases.append(alias)

            if needed_aliases:
                # Create a new import with only needed names
                new_import = ast.ImportFrom(module=imp.module, names=needed_aliases, level=imp.level)
                ast.copy_location(new_import, imp)
                needed_imports.append(new_import)

    return needed_imports


def find_definitions(tree: ast.AST) -> list[tuple[ast.stmt, str, str]]:
    """Find all class and function definitions at module level.

    Returns list of tuples: (node, type, name) where type is 'class' or 'function'.
    """
    definitions: list[tuple[ast.stmt, str, str]] = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            definitions.append((node, "class", node.name))
        elif isinstance(node, ast.FunctionDef):
            definitions.append((node, "function", node.name))
    return definitions


def create_import_statement(module_path: str, name: str) -> ast.ImportFrom:
    """Create an import statement for the extracted definition."""
    return ast.ImportFrom(
        module=module_path,
        names=[ast.alias(name=name, asname=None)],
        level=0,  # Absolute import from module
    )


def find_module_variables(tree: ast.AST) -> list[tuple[ast.stmt, str]]:
    """Find all module-level variable assignments.

    Returns list of tuples: (assignment_node, variable_name).
    Only includes simple assignments like 'console = Console()'.
    """
    variables: list[tuple[ast.stmt, str]] = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            # Handle simple assignments like: variable = expression
            for target in node.targets:
                if isinstance(target, ast.Name):
                    variables.append((node, target.id))
    return variables
