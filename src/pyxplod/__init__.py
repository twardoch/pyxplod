# this_file: src/pyxplod/__init__.py
"""pyxplod: Python code exploder - extracts classes and functions into separate files."""

from pyxplod.__version__ import __version__
from pyxplod.cli import main  # Updated import

__all__ = ["__version__", "main"]
