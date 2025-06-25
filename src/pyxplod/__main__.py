# this_file: src/pyxplod/__main__.py
"""Entry point for running pyxplod as a module."""

import fire

from pyxplod.cli import main  # Updated import

if __name__ == "__main__":
    fire.Fire(main)
