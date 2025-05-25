import ast
import re
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from loguru import logger
from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn

from pyxplod.pyxplod_analyze_name_usage import analyze_name_usage
from pyxplod.pyxplod_create_import_statement import create_import_statement
from pyxplod.pyxplod_extract_imports import extract_imports
from pyxplod.pyxplod_filter_imports_for_names import filter_imports_for_names
from pyxplod.pyxplod_find_definitions import find_definitions
from pyxplod.pyxplod_find_python_files import find_python_files
from pyxplod.pyxplod_generate_filename import generate_filename
from pyxplod.pyxplod_main import main
from pyxplod.pyxplod_process_python_file import process_python_file
from pyxplod.pyxplod_process_python_file_dirs import process_python_file_dirs
from pyxplod.pyxplod_to_snake_case import to_snake_case
from pyxplod.pyxplod_validate_paths import validate_paths
from pyxplod.pyxplod_write_extracted_file import write_extracted_file

'pyxplod: Python code exploder - extracts classes and functions into separate files.\n\nThis tool takes a Python project and "explodes" it by extracting each class and function\ndefinition into its own file, replacing the original definitions with imports.\n'
console = Console()
