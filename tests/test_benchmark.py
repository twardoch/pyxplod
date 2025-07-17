#!/usr/bin/env python3
# this_file: tests/test_benchmark.py

"""Benchmark tests for pyxplod performance."""

from pathlib import Path

import pytest

from pyxplod.cli import process_directory


class TestBenchmarks:
    """Benchmark tests for performance measurement."""

    def create_large_file(self, path: Path, num_classes: int = 100, num_functions: int = 100):
        """Create a large Python file with many classes and functions."""
        content = [
            "import os",
            "import sys",
            "from typing import Dict, List, Optional",
            "from collections import defaultdict",
            "",
            "# Module-level constants",
            "VERSION = '1.0.0'",
            "CONFIG = {'debug': True}",
            "",
        ]

        # Add classes
        for i in range(num_classes):
            content.extend(
                [
                    f"class Class{i}:",
                    "    def __init__(self):",
                    f"        self.value = {i}",
                    "    ",
                    f"    def method{i}(self):",
                    "        return self.value * 2",
                    "    ",
                    f"    def another_method{i}(self, data: Dict) -> List:",
                    "        return [self.value, data]",
                    "",
                ]
            )

        # Add functions
        for i in range(num_functions):
            content.extend(
                [
                    f"def function{i}(data: Optional[Dict] = None) -> int:",
                    "    if data is None:",
                    "        data = defaultdict(list)",
                    f"    return len(data) + {i}",
                    "",
                ]
            )

        # Add some module-level code
        content.extend(
            [
                "# Module initialization",
                "print(f'Module loaded with {num_classes} classes and {num_functions} functions')",
                "initialized = True",
            ]
        )

        path.write_text("\n".join(content))

    @pytest.mark.benchmark
    def test_process_large_file_files_method(self, tmp_path, benchmark):
        """Benchmark processing a large file with files method."""
        input_dir = tmp_path / "input"
        input_dir.mkdir()

        # Create a large file
        large_file = input_dir / "large_module.py"
        self.create_large_file(large_file, num_classes=50, num_functions=50)

        output_dir = tmp_path / "output"

        # Benchmark the processing
        result = benchmark(process_directory, input_dir, output_dir, "files", False)

        # Verify the result
        assert output_dir.exists()
        assert len(list(output_dir.glob("*.py"))) >= 101  # Original + 50 classes + 50 functions

    @pytest.mark.benchmark
    def test_process_large_file_dirs_method(self, tmp_path, benchmark):
        """Benchmark processing a large file with dirs method."""
        input_dir = tmp_path / "input"
        input_dir.mkdir()

        # Create a large file
        large_file = input_dir / "large_module.py"
        self.create_large_file(large_file, num_classes=50, num_functions=50)

        output_dir = tmp_path / "output"

        # Benchmark the processing
        result = benchmark(process_directory, input_dir, output_dir, "dirs", False)

        # Verify the result
        assert (output_dir / "large_module").is_dir()
        assert len(list((output_dir / "large_module").glob("*.py"))) >= 101  # __init__.py + 50 classes + 50 functions

    @pytest.mark.benchmark
    def test_process_multiple_files(self, tmp_path, benchmark):
        """Benchmark processing multiple files."""
        input_dir = tmp_path / "input"
        input_dir.mkdir()

        # Create multiple files
        for i in range(10):
            file_path = input_dir / f"module_{i}.py"
            self.create_large_file(file_path, num_classes=10, num_functions=10)

        output_dir = tmp_path / "output"

        # Benchmark the processing
        result = benchmark(process_directory, input_dir, output_dir, "files", False)

        # Verify the result
        assert output_dir.exists()
        # Should have at least 10 original files + 10*10 classes + 10*10 functions
        assert len(list(output_dir.glob("*.py"))) >= 210

    @pytest.mark.benchmark
    def test_process_nested_structure(self, tmp_path, benchmark):
        """Benchmark processing nested directory structure."""
        input_dir = tmp_path / "input"

        # Create nested structure
        for i in range(5):
            subdir = input_dir / f"subdir_{i}"
            subdir.mkdir(parents=True)
            for j in range(3):
                file_path = subdir / f"module_{j}.py"
                self.create_large_file(file_path, num_classes=5, num_functions=5)

        output_dir = tmp_path / "output"

        # Benchmark the processing
        result = benchmark(process_directory, input_dir, output_dir, "dirs", False)

        # Verify the result
        assert output_dir.exists()
        # Should have 5 subdirs, each with 3 modules, each expanded to directories
        for i in range(5):
            assert (output_dir / f"subdir_{i}").is_dir()
            for j in range(3):
                assert (output_dir / f"subdir_{i}" / f"module_{j}").is_dir()

    @pytest.mark.benchmark
    def test_import_analysis_performance(self, tmp_path, benchmark):
        """Benchmark import analysis on files with many imports."""
        input_dir = tmp_path / "input"
        input_dir.mkdir()

        # Create file with many imports
        imports_file = input_dir / "imports.py"
        imports = [
            "import os",
            "import sys",
            "import json",
            "import re",
            "import datetime",
            "import uuid",
            "import hashlib",
            "import base64",
            "import urllib.parse",
            "import collections",
            "from typing import Dict, List, Optional, Union, Tuple, Any",
            "from pathlib import Path",
            "from dataclasses import dataclass",
            "from functools import wraps, lru_cache",
            "from itertools import chain, combinations",
            "from collections import defaultdict, Counter, deque",
        ]

        content = imports + [
            "",
            "def use_some_imports():",
            "    data = defaultdict(list)",
            "    path = Path(os.getcwd())",
            "    return json.dumps({'path': str(path), 'data': dict(data)})",
            "",
            "class ImportUser:",
            "    def __init__(self):",
            "        self.counter = Counter()",
            "        self.uuid = str(uuid.uuid4())",
            "    ",
            "    def process(self, data: Dict) -> List:",
            "        return list(chain.from_iterable(data.values()))",
        ]

        imports_file.write_text("\n".join(content))

        output_dir = tmp_path / "output"

        # Benchmark the processing
        result = benchmark(process_directory, input_dir, output_dir, "files", False)

        # Verify import filtering worked
        func_content = (output_dir / "imports_use_some_imports.py").read_text()
        assert "import os" in func_content
        assert "import json" in func_content
        assert "from pathlib import Path" in func_content
        assert "from collections import defaultdict" in func_content
        # Should not include unused imports
        assert "import sys" not in func_content
        assert "import re" not in func_content
