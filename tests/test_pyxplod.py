#!/usr/bin/env python3
# this_file: tests/test_pyxplod.py

"""Test suite for pyxplod functionality."""

import ast

from pyxplod.pyxplod import (
    create_import_statement,
    extract_imports,
    find_definitions,
    find_python_files,
    generate_filename,
    process_python_file,
    to_snake_case,
    validate_paths,
)


class TestUtilityFunctions:
    """Test utility functions used in pyxplod."""

    def test_to_snake_case(self):
        """Test conversion of various formats to snake_case."""
        assert to_snake_case("CamelCase") == "camel_case"
        assert to_snake_case("camelCase") == "camel_case"
        assert to_snake_case("snake_case") == "snake_case"
        assert to_snake_case("HTTPResponse") == "http_response"
        assert to_snake_case("getHTTPResponseCode") == "get_http_response_code"
        assert to_snake_case("SimpleTest") == "simple_test"
        assert to_snake_case("a") == "a"
        assert to_snake_case("A") == "a"

    def test_extract_imports(self):
        """Test extraction of import statements from AST."""
        code = """
import os
from pathlib import Path
import sys
from typing import List, Dict

def my_function():
    pass
"""
        tree = ast.parse(code)
        imports = extract_imports(tree)

        assert len(imports) == 4
        assert all(isinstance(imp, ast.Import | ast.ImportFrom) for imp in imports)

    def test_find_definitions(self):
        """Test finding class and function definitions."""
        code = """
import os

class MyClass:
    pass

def my_function():
    pass

class AnotherClass:
    def method(self):
        pass

def another_function():
    return 42

x = 10  # Not a definition
"""
        tree = ast.parse(code)
        definitions = find_definitions(tree)

        assert len(definitions) == 4
        assert definitions[0][1] == "class"
        assert definitions[0][2] == "MyClass"
        assert definitions[1][1] == "function"
        assert definitions[1][2] == "my_function"
        assert definitions[2][1] == "class"
        assert definitions[2][2] == "AnotherClass"
        assert definitions[3][1] == "function"
        assert definitions[3][2] == "another_function"

    def test_generate_filename(self):
        """Test filename generation with deduplication."""
        existing = set()

        # First file
        name1 = generate_filename("module", "MyClass", "class", existing)
        assert name1 == "module_my_class.py"

        # Duplicate should get a number
        name2 = generate_filename("module", "MyClass", "class", existing)
        assert name2 == "module_my_class_2.py"

        # Another duplicate
        name3 = generate_filename("module", "MyClass", "class", existing)
        assert name3 == "module_my_class_3.py"

        # Different name should work normally
        name4 = generate_filename("module", "OtherClass", "class", existing)
        assert name4 == "module_other_class.py"

    def test_create_import_statement(self):
        """Test creation of import statements."""
        import_stmt = create_import_statement(".module_my_class", "MyClass")

        assert isinstance(import_stmt, ast.ImportFrom)
        assert import_stmt.module == ".module_my_class"
        assert import_stmt.level == 0
        assert len(import_stmt.names) == 1
        assert import_stmt.names[0].name == "MyClass"
        assert import_stmt.names[0].asname is None


class TestFileOperations:
    """Test file discovery and validation functions."""

    def test_find_python_files(self, tmp_path):
        """Test recursive Python file discovery."""
        # Create test directory structure
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "module1.py").write_text("# Python file")
        (tmp_path / "src" / "module2.py").write_text("# Another file")
        (tmp_path / "src" / "subdir").mkdir()
        (tmp_path / "src" / "subdir" / "module3.py").write_text("# Nested file")
        (tmp_path / "src" / "__pycache__").mkdir()
        (tmp_path / "src" / "__pycache__" / "module1.pyc").write_text("# Compiled")
        (tmp_path / "README.md").write_text("# Not a Python file")

        files = find_python_files(tmp_path)

        assert len(files) == 3
        assert all(f.suffix == ".py" for f in files)
        assert all("__pycache__" not in str(f) for f in files)
        assert all(".pyc" not in str(f) for f in files)

    def test_validate_paths(self, tmp_path):
        """Test path validation."""
        # Valid paths
        input_dir = tmp_path / "input"
        input_dir.mkdir()
        output_dir = tmp_path / "output"

        assert validate_paths(input_dir, output_dir) is True

        # Non-existent input
        assert validate_paths(tmp_path / "nonexistent", output_dir) is False

        # Input is file, not directory
        input_file = tmp_path / "file.txt"
        input_file.write_text("content")
        assert validate_paths(input_file, output_dir) is False

        # Output exists but is file
        output_file = tmp_path / "output.txt"
        output_file.write_text("content")
        assert validate_paths(input_dir, output_file) is False


class TestProcessing:
    """Test the main processing functionality."""

    def test_process_simple_file(self, tmp_path):
        """Test processing a simple Python file."""
        # Create input directory and file
        input_dir = tmp_path / "input"
        input_dir.mkdir()

        test_file = input_dir / "test.py"
        test_file.write_text(
            """
import os

class TestClass:
    def method(self):
        return "test"

def test_function():
    return 42

print("Module loaded")
"""
        )

        # Process the file
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        process_python_file(test_file, output_dir, input_dir)

        # Check output files exist
        assert (output_dir / "test.py").exists()
        assert (output_dir / "test_test_class.py").exists()
        assert (output_dir / "test_test_function.py").exists()

        # Check main file content
        main_content = (output_dir / "test.py").read_text()
        assert "import os" in main_content
        assert "from .test_test_class import TestClass" in main_content
        assert "from .test_test_function import test_function" in main_content
        assert (
            "print('Module loaded')" in main_content
            or 'print("Module loaded")' in main_content
        )
        assert "def test_function" not in main_content
        assert "class TestClass" not in main_content

        # Check extracted class file
        class_content = (output_dir / "test_test_class.py").read_text()
        assert "import os" in class_content
        assert "class TestClass:" in class_content
        assert "def method(self):" in class_content

        # Check extracted function file
        func_content = (output_dir / "test_test_function.py").read_text()
        assert "import os" in func_content
        assert "def test_function():" in func_content
        assert "return 42" in func_content

    def test_process_file_no_definitions(self, tmp_path):
        """Test processing a file with no class/function definitions."""
        input_dir = tmp_path / "input"
        input_dir.mkdir()

        test_file = input_dir / "constants.py"
        test_file.write_text(
            """
# Constants file
VERSION = "1.0.0"
DEBUG = True
CONFIG = {"key": "value"}
"""
        )

        output_dir = tmp_path / "output"
        output_dir.mkdir()

        process_python_file(test_file, output_dir, input_dir)

        # Should just copy the file
        assert (output_dir / "constants.py").exists()
        assert (output_dir / "constants.py").read_text() == test_file.read_text()

    def test_process_nested_structure(self, tmp_path):
        """Test processing files in nested directory structure."""
        input_dir = tmp_path / "input"
        (input_dir / "src" / "utils").mkdir(parents=True)

        test_file = input_dir / "src" / "utils" / "helpers.py"
        test_file.write_text(
            """
def helper_function():
    return "help"

class HelperClass:
    pass
"""
        )

        output_dir = tmp_path / "output"

        process_python_file(test_file, output_dir, input_dir)

        # Check directory structure is preserved
        assert (output_dir / "src" / "utils" / "helpers.py").exists()
        assert (output_dir / "src" / "utils" / "helpers_helper_function.py").exists()
        assert (output_dir / "src" / "utils" / "helpers_helper_class.py").exists()

    def test_process_file_with_syntax_error(self, tmp_path):
        """Test handling of files with syntax errors."""
        input_dir = tmp_path / "input"
        input_dir.mkdir()

        test_file = input_dir / "broken.py"
        test_file.write_text(
            """
def broken_function(
    # Missing closing parenthesis
    return "broken"
"""
        )

        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Should handle error gracefully
        process_python_file(test_file, output_dir, input_dir)

        # No output files should be created for broken file
        assert not (output_dir / "broken.py").exists()
