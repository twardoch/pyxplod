def generate_filename(base_name: str, def_name: str, def_type: str, existing_files: set) -> str:
    """Generate a unique filename for the extracted definition.

    Handles deduplication by appending numbers if necessary.
    """
    snake_name = to_snake_case(def_name)
    filename = f"{base_name}_{snake_name}.py"
    if filename in existing_files:
        counter = 2
        while f"{base_name}_{snake_name}_{counter}.py" in existing_files:
            counter += 1
        filename = f"{base_name}_{snake_name}_{counter}.py"
    existing_files.add(filename)
    return filename
