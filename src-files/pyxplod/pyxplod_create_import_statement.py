import ast


def create_import_statement(module_path: str, name: str) -> ast.ImportFrom:
    """Create an import statement for the extracted definition."""
    return ast.ImportFrom(module=module_path, names=[ast.alias(name=name, asname=None)], level=0)
