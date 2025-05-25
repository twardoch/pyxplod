import ast


def analyze_name_usage(node: ast.AST) -> set[str]:
    """Analyze which names are used in an AST node.

    Returns a set of all names referenced in the node, including decorators.
    """
    names = set()

    class NameCollector(ast.NodeVisitor):
        def visit_Name(self, node: ast.Name) -> None:
            names.add(node.id)
            self.generic_visit(node)

        def visit_Attribute(self, node: ast.Attribute) -> None:
            if isinstance(node.value, ast.Name):
                names.add(node.value.id)
            self.generic_visit(node)

    if hasattr(node, "decorator_list"):
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name):
                names.add(decorator.id)
            elif isinstance(decorator, ast.Attribute) and isinstance(decorator.value, ast.Name):
                names.add(decorator.value.id)
            NameCollector().visit(decorator)
    NameCollector().visit(node)
    return names
