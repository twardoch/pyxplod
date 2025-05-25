import ast


def find_definitions(tree: ast.AST) -> list[tuple[ast.stmt, str, str]]:
    """Find all class and function definitions at module level.

    Returns list of tuples: (node, type, name) where type is 'class' or 'function'.
    """
    definitions = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            definitions.append((node, "class", node.name))
        elif isinstance(node, ast.FunctionDef):
            definitions.append((node, "function", node.name))
    return definitions
