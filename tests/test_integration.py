#!/usr/bin/env python3
# this_file: tests/test_integration.py

"""Integration tests for pyxplod."""

from pyxplod.cli import process_directory


class TestIntegration:
    """Integration tests for complete workflows."""

    def test_complex_project_files_method(self, tmp_path):
        """Test processing a complex project with files method."""
        # Create complex project structure
        input_dir = tmp_path / "input"
        (input_dir / "src" / "utils").mkdir(parents=True)
        (input_dir / "src" / "models").mkdir(parents=True)

        # Create main module
        main_file = input_dir / "src" / "main.py"
        main_file.write_text("""
import os
from utils.helpers import helper_function
from models.user import User

def main():
    print("Starting application")
    user = User("John")
    result = helper_function(user.name)
    return result

class Application:
    def __init__(self):
        self.name = "PyXplod Test"
    
    def run(self):
        return main()

if __name__ == "__main__":
    app = Application()
    app.run()
""")

        # Create utilities
        utils_file = input_dir / "src" / "utils" / "helpers.py"
        utils_file.write_text("""
from typing import Any

def helper_function(name: str) -> str:
    return f"Hello, {name}!"

def another_helper(data: Any) -> Any:
    return data

class UtilityClass:
    def __init__(self):
        self.initialized = True
    
    def process(self, data):
        return another_helper(data)
""")

        # Create models
        models_file = input_dir / "src" / "models" / "user.py"
        models_file.write_text("""
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    name: str
    age: Optional[int] = None
    
    def greet(self) -> str:
        return f"Hi, I'm {self.name}"

def create_user(name: str, age: int = None) -> User:
    return User(name, age)
""")

        output_dir = tmp_path / "output"

        # Process with files method
        process_directory(input_dir, output_dir, "files", verbose=True)

        # Check structure is preserved
        assert (output_dir / "src" / "main.py").exists()
        assert (output_dir / "src" / "utils" / "helpers.py").exists()
        assert (output_dir / "src" / "models" / "user.py").exists()

        # Check extracted files
        assert (output_dir / "src" / "main_main.py").exists()
        assert (output_dir / "src" / "main_application.py").exists()
        assert (output_dir / "src" / "utils" / "helpers_helper_function.py").exists()
        assert (output_dir / "src" / "utils" / "helpers_another_helper.py").exists()
        assert (output_dir / "src" / "utils" / "helpers_utility_class.py").exists()
        assert (output_dir / "src" / "models" / "user_user.py").exists()
        assert (output_dir / "src" / "models" / "user_create_user.py").exists()

        # Check imports are preserved
        main_content = (output_dir / "src" / "main.py").read_text()
        assert "from utils.helpers import helper_function" in main_content
        assert "from models.user import User" in main_content
        assert "from .main_main import main" in main_content
        assert "from .main_application import Application" in main_content

    def test_complex_project_dirs_method(self, tmp_path):
        """Test processing a complex project with dirs method."""
        # Create the same complex project structure
        input_dir = tmp_path / "input"
        (input_dir / "src").mkdir(parents=True)

        # Create a module with multiple definitions
        module_file = input_dir / "src" / "complex_module.py"
        module_file.write_text("""
import json
from typing import Dict, List

# Module-level constants
DEFAULT_CONFIG = {"debug": True}
VERSION = "1.0.0"

class DataProcessor:
    def __init__(self, config: Dict = None):
        self.config = config or DEFAULT_CONFIG
    
    def process(self, data: List) -> Dict:
        return {"processed": len(data)}

class DataValidator:
    def validate(self, data: Dict) -> bool:
        return "data" in data

def load_config(filename: str) -> Dict:
    with open(filename, 'r') as f:
        return json.load(f)

def save_config(config: Dict, filename: str) -> None:
    with open(filename, 'w') as f:
        json.dump(config, f)

def process_data(data: List) -> Dict:
    processor = DataProcessor()
    return processor.process(data)

# Initialize module
print(f"Module loaded, version: {VERSION}")
""")

        output_dir = tmp_path / "output"

        # Process with dirs method
        process_directory(input_dir, output_dir, "dirs", verbose=True)

        # Check directory structure
        assert (output_dir / "src" / "complex_module").is_dir()
        assert (output_dir / "src" / "complex_module" / "__init__.py").exists()
        assert (output_dir / "src" / "complex_module" / "data_processor.py").exists()
        assert (output_dir / "src" / "complex_module" / "data_validator.py").exists()
        assert (output_dir / "src" / "complex_module" / "load_config.py").exists()
        assert (output_dir / "src" / "complex_module" / "save_config.py").exists()
        assert (output_dir / "src" / "complex_module" / "process_data.py").exists()

        # Check __init__.py contains module-level code
        init_content = (output_dir / "src" / "complex_module" / "__init__.py").read_text()
        assert "import json" in init_content
        assert "DEFAULT_CONFIG = " in init_content
        assert "VERSION = " in init_content
        assert (
            'print(f"Module loaded, version: {VERSION}")' in init_content
            or "print(f'Module loaded, version: {VERSION}')" in init_content
        )

        # Check imports are correct
        assert "from .data_processor import DataProcessor" in init_content
        assert "from .data_validator import DataValidator" in init_content
        assert "from .load_config import load_config" in init_content

        # Check individual files
        processor_content = (output_dir / "src" / "complex_module" / "data_processor.py").read_text()
        assert "class DataProcessor:" in processor_content
        assert "DEFAULT_CONFIG" in processor_content  # Should include used module variable

        process_data_content = (output_dir / "src" / "complex_module" / "process_data.py").read_text()
        assert "def process_data(data: List) -> Dict:" in process_data_content
        assert "from .data_processor import DataProcessor" in process_data_content

    def test_edge_cases(self, tmp_path):
        """Test edge cases and error conditions."""
        input_dir = tmp_path / "input"
        input_dir.mkdir()

        # File with decorators
        decorator_file = input_dir / "decorators.py"
        decorator_file.write_text("""
from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def decorated_function():
    return "decorated"

class DecoratedClass:
    @my_decorator
    def method(self):
        return "method"
""")

        # File with complex imports
        imports_file = input_dir / "imports.py"
        imports_file.write_text("""
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict, Counter

def use_imports():
    path = Path(os.getcwd())
    data = defaultdict(list)
    return {"path": path, "data": data}

class ImportUser:
    def __init__(self):
        self.counter = Counter()
        self.optional_data: Optional[Dict] = None
""")

        output_dir = tmp_path / "output"

        # Process both files
        process_directory(input_dir, output_dir, "files", verbose=True)

        # Check decorator handling
        assert (output_dir / "decorators.py").exists()
        assert (output_dir / "decorators_my_decorator.py").exists()
        assert (output_dir / "decorators_decorated_function.py").exists()

        decorator_func_content = (output_dir / "decorators_decorated_function.py").read_text()
        assert "from .decorators_my_decorator import my_decorator" in decorator_func_content
        assert "@my_decorator" in decorator_func_content

        # Check import filtering
        imports_func_content = (output_dir / "imports_use_imports.py").read_text()
        assert "import os" in imports_func_content
        assert "from pathlib import Path" in imports_func_content
        assert "from collections import defaultdict" in imports_func_content
        # Should not include unused imports
        assert "import sys" not in imports_func_content
        assert "Counter" not in imports_func_content

        imports_class_content = (output_dir / "imports_import_user.py").read_text()
        assert "from collections import Counter" in imports_class_content
        assert "from typing import Dict, Optional" in imports_class_content
        # Should not include unused imports
        assert "import os" not in imports_class_content
        assert "from pathlib import Path" not in imports_class_content
