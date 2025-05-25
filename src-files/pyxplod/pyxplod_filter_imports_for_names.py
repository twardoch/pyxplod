import ast


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
            needed_aliases = []
            for alias in imp.names:
                name_in_code = alias.asname if alias.asname else alias.name
                base_name = name_in_code.split(".")[0]
                if base_name in used_names:
                    needed_aliases.append(alias)
            if needed_aliases:
                new_import = ast.Import(names=needed_aliases)
                ast.copy_location(new_import, imp)
                needed_imports.append(new_import)
        elif isinstance(imp, ast.ImportFrom):
            needed_aliases = []
            for alias in imp.names:
                name_in_code = alias.asname if alias.asname else alias.name
                if name_in_code in used_names:
                    needed_aliases.append(alias)
            if needed_aliases:
                new_import = ast.ImportFrom(module=imp.module, names=needed_aliases, level=imp.level)
                ast.copy_location(new_import, imp)
                needed_imports.append(new_import)
    return needed_imports
