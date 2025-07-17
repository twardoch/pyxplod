#!/usr/bin/env python3
# this_file: tests/test_cli.py

"""Test suite for CLI functionality."""

from unittest.mock import patch

import pytest

from pyxplod.cli import main


class TestCLI:
    """Test CLI functionality."""

    def test_main_with_files_method(self, tmp_path):
        """Test main function with files method."""
        # Create input directory and file
        input_dir = tmp_path / "input"
        input_dir.mkdir()

        test_file = input_dir / "test.py"
        test_file.write_text("""
def test_function():
    return "test"

class TestClass:
    pass
""")

        output_dir = tmp_path / "output"

        # Run main function
        with patch("sys.argv", ["pyxplod", str(input_dir), str(output_dir), "--method", "files", "--verbose"]):
            main()

        # Check outputs
        assert output_dir.exists()
        assert (output_dir / "test.py").exists()
        assert (output_dir / "test_test_function.py").exists()
        assert (output_dir / "test_test_class.py").exists()

    def test_main_with_dirs_method(self, tmp_path):
        """Test main function with dirs method."""
        # Create input directory and file
        input_dir = tmp_path / "input"
        input_dir.mkdir()

        test_file = input_dir / "test.py"
        test_file.write_text("""
def test_function():
    return "test"

class TestClass:
    pass
""")

        output_dir = tmp_path / "output"

        # Run main function
        with patch("sys.argv", ["pyxplod", str(input_dir), str(output_dir), "--method", "dirs", "--verbose"]):
            main()

        # Check outputs
        assert output_dir.exists()
        assert (output_dir / "test").is_dir()
        assert (output_dir / "test" / "__init__.py").exists()
        assert (output_dir / "test" / "test_function.py").exists()
        assert (output_dir / "test" / "test_class.py").exists()

    def test_main_invalid_method(self, tmp_path):
        """Test main function with invalid method."""
        input_dir = tmp_path / "input"
        input_dir.mkdir()
        output_dir = tmp_path / "output"

        with pytest.raises(SystemExit):
            with patch("sys.argv", ["pyxplod", str(input_dir), str(output_dir), "--method", "invalid"]):
                main()

    def test_main_invalid_paths(self, tmp_path):
        """Test main function with invalid paths."""
        input_dir = tmp_path / "nonexistent"
        output_dir = tmp_path / "output"

        with pytest.raises(SystemExit):
            with patch("sys.argv", ["pyxplod", str(input_dir), str(output_dir), "--method", "files"]):
                main()
