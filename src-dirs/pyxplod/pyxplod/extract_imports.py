import ast


def extract_imports(tree: ast.AST) -> list[ast.stmt]:
    """Extract all import statements from an AST.

    Returns a list of Import and ImportFrom nodes at module level only.
    """
    imports = []
    for node in tree.body:
        if isinstance(node, ast.Import | ast.ImportFrom):
            imports.append(node)
    return imports
