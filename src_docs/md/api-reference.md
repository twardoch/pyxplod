# API Reference

Complete API documentation for programmatic usage of pyxplod, including function signatures, classes, and examples for integrating pyxplod into your own tools and workflows.

## Core API

### Main Entry Point

#### `pyxplod.cli.main()`

The primary function for programmatic code explosion.

```python
def main(
    input_dir_str: str, 
    output: str, 
    method: str = "files", 
    *, 
    verbose: bool = False
) -> None
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `input_dir_str` | `str` | ✅ | Path to input directory containing Python files |
| `output` | `str` | ✅ | Path to output directory for exploded files |
| `method` | `str` | ❌ | Explosion method: `"files"` or `"dirs"` (default: `"files"`) |
| `verbose` | `bool` | ❌ | Enable verbose logging (default: `False`) |

**Returns:** `None`

**Raises:**
- `ValueError`: If method is not `"files"` or `"dirs"`
- `FileNotFoundError`: If input directory doesn't exist
- `PermissionError`: If output directory can't be created or written to

**Example:**
```python
from pyxplod.cli import main

# Basic usage
main("./src", "./exploded", method="files")

# With verbose logging
main(
    input_dir_str="./my_project/src",
    output="./exploded_project", 
    method="dirs",
    verbose=True
)
```

## File Processing API

### File Discovery

#### `pyxplod.file_utils.find_python_files()`

Recursively find all Python files in a directory.

```python
def find_python_files(directory: Path) -> list[Path]
```

**Parameters:**
- `directory` (`Path`): Directory to search for Python files

**Returns:** List of Path objects for found Python files

**Example:**
```python
from pathlib import Path
from pyxplod.file_utils import find_python_files

files = find_python_files(Path("./src"))
print(f"Found {len(files)} Python files")
for file in files:
    print(f"  {file}")
```

#### `pyxplod.file_utils.validate_paths()`

Validate input and output directory paths.

```python
def validate_paths(input_path: Path, output_path: Path) -> bool
```

**Parameters:**
- `input_path` (`Path`): Input directory path
- `output_path` (`Path`): Output directory path

**Returns:** `True` if paths are valid, `False` otherwise

**Example:**
```python
from pathlib import Path
from pyxplod.file_utils import validate_paths

input_dir = Path("./src")
output_dir = Path("./exploded")

if validate_paths(input_dir, output_dir):
    print("Paths are valid")
else:
    print("Invalid paths")
```

### Core Processing Functions

#### `pyxplod.processors.process_python_file()`

Process a single Python file using the files method.

```python
def process_python_file(
    file_path: Path, 
    output_base: Path, 
    input_base: Path
) -> None
```

**Parameters:**
- `file_path` (`Path`): Path to the Python file to process
- `output_base` (`Path`): Base output directory
- `input_base` (`Path`): Base input directory

**Example:**
```python
from pathlib import Path
from pyxplod.processors import process_python_file

process_python_file(
    file_path=Path("./src/utils.py"),
    output_base=Path("./exploded"),
    input_base=Path("./src")
)
```

#### `pyxplod.processors.process_python_file_dirs()`

Process a single Python file using the dirs method.

```python
def process_python_file_dirs(
    file_path: Path, 
    output_base: Path, 
    input_base: Path
) -> None
```

**Parameters:**
- `file_path` (`Path`): Path to the Python file to process
- `output_base` (`Path`): Base output directory  
- `input_base` (`Path`): Base input directory

**Example:**
```python
from pathlib import Path
from pyxplod.processors import process_python_file_dirs

process_python_file_dirs(
    file_path=Path("./src/database.py"),
    output_base=Path("./exploded"),
    input_base=Path("./src")
)
```

## AST Utilities API

### AST Analysis

#### `pyxplod.ast_utils.extract_imports()`

Extract import statements from an AST module.

```python
def extract_imports(tree: ast.Module) -> list[ast.stmt]
```

**Parameters:**
- `tree` (`ast.Module`): Parsed AST module

**Returns:** List of import statement nodes

**Example:**
```python
import ast
from pyxplod.ast_utils import extract_imports

with open("module.py") as f:
    tree = ast.parse(f.read())

imports = extract_imports(tree)
print(f"Found {len(imports)} import statements")
```

#### `pyxplod.ast_utils.find_top_level_definitions()`

Find all top-level class and function definitions.

```python
def find_top_level_definitions(tree: ast.Module) -> list[ast.stmt]
```

**Parameters:**
- `tree` (`ast.Module`): Parsed AST module

**Returns:** List of definition nodes (ClassDef, FunctionDef, AsyncFunctionDef)

**Example:**
```python
import ast
from pyxplod.ast_utils import find_top_level_definitions

with open("module.py") as f:
    tree = ast.parse(f.read())

definitions = find_top_level_definitions(tree)
for definition in definitions:
    print(f"Found: {definition.name} ({type(definition).__name__})")
```

#### `pyxplod.ast_utils.get_used_names()`

Get all names used within an AST node.

```python
def get_used_names(node: ast.AST) -> set[str]
```

**Parameters:**
- `node` (`ast.AST`): AST node to analyze

**Returns:** Set of name strings used in the node

**Example:**
```python
import ast
from pyxplod.ast_utils import get_used_names, find_top_level_definitions

with open("module.py") as f:
    tree = ast.parse(f.read())

definitions = find_top_level_definitions(tree)
for definition in definitions:
    used_names = get_used_names(definition)
    print(f"{definition.name} uses: {used_names}")
```

#### `pyxplod.ast_utils.filter_imports_for_names()`

Filter imports to only those needed for specific names.

```python
def filter_imports_for_names(
    imports: list[ast.stmt], 
    used_names: set[str]
) -> list[ast.stmt]
```

**Parameters:**
- `imports` (`list[ast.stmt]`): List of import statement nodes
- `used_names` (`set[str]`): Set of names that are used

**Returns:** Filtered list of import statements

**Example:**
```python
import ast
from pyxplod.ast_utils import (
    extract_imports, get_used_names, filter_imports_for_names,
    find_top_level_definitions
)

with open("module.py") as f:
    tree = ast.parse(f.read())

imports = extract_imports(tree)
definitions = find_top_level_definitions(tree)

for definition in definitions:
    used_names = get_used_names(definition)
    needed_imports = filter_imports_for_names(imports, used_names)
    print(f"{definition.name} needs {len(needed_imports)} imports")
```

### Module Variables

#### `pyxplod.ast_utils.find_module_variables()`

Find all module-level variable assignments.

```python
def find_module_variables(tree: ast.Module) -> dict[str, ast.stmt]
```

**Parameters:**
- `tree` (`ast.Module`): Parsed AST module

**Returns:** Dictionary mapping variable names to assignment nodes

**Example:**
```python
import ast
from pyxplod.ast_utils import find_module_variables

with open("module.py") as f:
    tree = ast.parse(f.read())

variables = find_module_variables(tree)
print("Module variables:")
for name, node in variables.items():
    print(f"  {name}")
```

#### `pyxplod.ast_utils.get_needed_variables()`

Get module variables needed by a specific definition.

```python
def get_needed_variables(
    definition: ast.stmt, 
    module_vars: dict[str, ast.stmt]
) -> list[ast.stmt]
```

**Parameters:**
- `definition` (`ast.stmt`): Function or class definition
- `module_vars` (`dict[str, ast.stmt]`): Module variables mapping

**Returns:** List of needed variable assignment nodes

**Example:**
```python
import ast
from pyxplod.ast_utils import (
    find_top_level_definitions, find_module_variables, get_needed_variables
)

with open("module.py") as f:
    tree = ast.parse(f.read())

definitions = find_top_level_definitions(tree)
module_vars = find_module_variables(tree)

for definition in definitions:
    needed_vars = get_needed_variables(definition, module_vars)
    print(f"{definition.name} needs {len(needed_vars)} module variables")
```

## Utility Functions

### Name Conversion

#### `pyxplod.utils.to_snake_case()`

Convert names to snake_case format.

```python
def to_snake_case(name: str) -> str
```

**Parameters:**
- `name` (`str`): Name to convert (PascalCase, camelCase, etc.)

**Returns:** snake_case version of the name

**Example:**
```python
from pyxplod.utils import to_snake_case

# Class names
print(to_snake_case("ConfigManager"))     # "config_manager"
print(to_snake_case("HTTPClient"))        # "http_client"
print(to_snake_case("XMLParser"))         # "xml_parser"

# Function names
print(to_snake_case("processData"))       # "process_data"
print(to_snake_case("validateInput"))     # "validate_input"
```

### File Operations

#### `pyxplod.file_utils.generate_safe_filename()`

Generate a safe filename, handling potential collisions.

```python
def generate_safe_filename(
    base_name: str, 
    extension: str, 
    directory: Path
) -> str
```

**Parameters:**
- `base_name` (`str`): Base filename without extension
- `extension` (`str`): File extension (including dot)
- `directory` (`Path`): Directory where file will be created

**Returns:** Safe filename that doesn't conflict with existing files

**Example:**
```python
from pathlib import Path
from pyxplod.file_utils import generate_safe_filename

safe_name = generate_safe_filename(
    base_name="utils_helper",
    extension=".py", 
    directory=Path("./output")
)
print(f"Safe filename: {safe_name}")
```

## Advanced Usage Examples

### Custom Processing Pipeline

```python
from pathlib import Path
import ast
from loguru import logger

from pyxplod.file_utils import find_python_files, validate_paths
from pyxplod.ast_utils import (
    extract_imports, find_top_level_definitions, 
    get_used_names, filter_imports_for_names
)
from pyxplod.utils import to_snake_case

def custom_explode(input_dir: str, output_dir: str):
    """Custom explosion with additional processing."""
    input_path = Path(input_dir).resolve()
    output_path = Path(output_dir).resolve()
    
    if not validate_paths(input_path, output_path):
        raise ValueError("Invalid paths")
    
    python_files = find_python_files(input_path)
    logger.info(f"Processing {len(python_files)} files")
    
    for file_path in python_files:
        with open(file_path) as f:
            tree = ast.parse(f.read())
        
        imports = extract_imports(tree)
        definitions = find_top_level_definitions(tree)
        
        for definition in definitions:
            # Custom processing logic here
            used_names = get_used_names(definition)
            needed_imports = filter_imports_for_names(imports, used_names)
            
            # Generate filename
            snake_name = to_snake_case(definition.name)
            filename = f"{file_path.stem}_{snake_name}.py"
            
            logger.info(f"Extracted {definition.name} → {filename}")

# Usage
custom_explode("./src", "./custom_output")
```

### Batch Processing

```python
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from pyxplod.processors import process_python_file

def batch_explode(input_dirs: list[str], output_base: str, method: str = "files"):
    """Process multiple directories in parallel."""
    
    def process_directory(input_dir: str):
        input_path = Path(input_dir)
        output_path = Path(output_base) / input_path.name
        
        from pyxplod.cli import main
        main(str(input_path), str(output_path), method=method)
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_directory, dir_path) 
                  for dir_path in input_dirs]
        
        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"Error processing directory: {e}")

# Usage
batch_explode(
    input_dirs=["./project1/src", "./project2/src", "./project3/src"],
    output_base="./exploded_projects",
    method="dirs"
)
```

### Integration with Build Systems

```python
import subprocess
from pathlib import Path
from pyxplod.cli import main

def explode_and_test(src_dir: str, test_dir: str):
    """Explode code and run tests to verify functionality."""
    
    # Backup original
    backup_dir = f"{src_dir}_backup"
    subprocess.run(["cp", "-r", src_dir, backup_dir])
    
    try:
        # Explode code
        exploded_dir = f"{src_dir}_exploded"
        main(src_dir, exploded_dir, method="dirs", verbose=True)
        
        # Replace original with exploded
        subprocess.run(["rm", "-rf", src_dir])
        subprocess.run(["mv", exploded_dir, src_dir])
        
        # Run tests
        result = subprocess.run(["python", "-m", "pytest", test_dir], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Explosion successful, tests pass")
            subprocess.run(["rm", "-rf", backup_dir])
        else:
            print("❌ Tests failed, restoring backup")
            subprocess.run(["rm", "-rf", src_dir])
            subprocess.run(["mv", backup_dir, src_dir])
            
    except Exception as e:
        print(f"Error during explosion: {e}")
        # Restore backup
        subprocess.run(["rm", "-rf", src_dir])
        subprocess.run(["mv", backup_dir, src_dir])

# Usage
explode_and_test("./src", "./tests")
```

## Error Handling

### Exception Types

pyxplod can raise several types of exceptions:

```python
from pyxplod.cli import main

try:
    main("./src", "./output", method="invalid")
except ValueError as e:
    print(f"Invalid method: {e}")

try:
    main("./nonexistent", "./output", method="files")
except FileNotFoundError as e:
    print(f"Directory not found: {e}")

try:
    main("./src", "/root/output", method="files")
except PermissionError as e:
    print(f"Permission denied: {e}")
```

### Graceful Error Handling

```python
from pathlib import Path
from loguru import logger
from pyxplod.cli import main

def safe_explode(input_dir: str, output_dir: str, method: str = "files"):
    """Safely explode code with comprehensive error handling."""
    
    try:
        # Validate inputs
        if method not in ["files", "dirs"]:
            raise ValueError(f"Invalid method: {method}")
        
        input_path = Path(input_dir)
        if not input_path.exists():
            raise FileNotFoundError(f"Input directory not found: {input_dir}")
        
        if not input_path.is_dir():
            raise ValueError(f"Input path is not a directory: {input_dir}")
        
        # Attempt explosion
        main(input_dir, output_dir, method=method, verbose=True)
        logger.success(f"Successfully exploded {input_dir} to {output_dir}")
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return False
        
    except FileNotFoundError as e:
        logger.error(f"File system error: {e}")
        return False
        
    except PermissionError as e:
        logger.error(f"Permission error: {e}")
        return False
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.exception("Full traceback:")
        return False
    
    return True

# Usage
if safe_explode("./src", "./output", method="dirs"):
    print("Explosion completed successfully")
else:
    print("Explosion failed")
```

## Next Steps

This API reference provides the foundation for:

- **Building custom tools** that integrate pyxplod
- **Automating code refactoring** workflows
- **Creating specialized explosion** strategies
- **Integrating with CI/CD** pipelines

For more examples and use cases, see the other documentation chapters!