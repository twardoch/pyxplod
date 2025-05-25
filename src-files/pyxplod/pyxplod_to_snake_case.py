import re


def to_snake_case(name: str) -> str:
    """Convert a name to snake_case format.

    Handles CamelCase, pascalCase, and already snake_case names.
    """
    s1 = re.sub("(.)([A-Z][a-z]+)", "\\1_\\2", name)
    s2 = re.sub("([a-z0-9])([A-Z])", "\\1_\\2", s1)
    return s2.lower()
