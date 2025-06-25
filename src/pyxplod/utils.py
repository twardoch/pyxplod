# this_file: src/pyxplod/utils.py
"""Utility functions for pyxplod."""

import re


def to_snake_case(name: str) -> str:
    """Convert a name to snake_case format.

    Handles CamelCase, pascalCase, and already snake_case names.
    """
    # Insert underscores before uppercase letters that follow lowercase letters
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    # Insert underscores before uppercase letters that follow lowercase or uppercase letters
    s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
    # Convert to lowercase
    return s2.lower()
