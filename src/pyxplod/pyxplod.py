# this_file: src/pyxplod/pyxplod.py

"""pyxplod: Python code exploder - extracts classes and functions into separate files.

This tool takes a Python project and "explodes" it by extracting each class and function
definition into its own file, replacing the original definitions with imports.
"""

# Core logic has been refactored into submodules.
# This file now primarily serves to expose the main CLI entry point.

from pyxplod.cli import main

__all__ = ["main"]
