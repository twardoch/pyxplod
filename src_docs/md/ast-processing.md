# AST Processing

Deep dive into how pyxplod uses Python's Abstract Syntax Tree (AST) to analyze and transform code. This chapter covers the technical implementation details of code parsing, analysis, and reconstruction.

## Introduction to AST

An **Abstract Syntax Tree (AST)** is a tree representation of the syntactic structure of source code. Each node represents a construct in the programming language.

### Why AST Over Text Processing?

| Approach | Advantages | Disadvantages |
|----------|------------|---------------|
| **Text/Regex** | Simple to implement | Fragile, misses context, error-prone |
| **AST Processing** | Precise, context-aware, robust | More complex, requires parsing |

pyxplod uses AST processing for reliability and accuracy.

### Basic AST Example

```python
import ast

code = """
class MyClass:
    def method(self):
        return "hello"
"""

tree = ast.parse(code)
print(ast.dump(tree, indent=2))
```

**Output:**
```python
Module(
  body=[
    ClassDef(
      name='MyClass',
      bases=[],
      keywords=[],
      decorator_list=[],
      body=[
        FunctionDef(
          name='method',
          args=arguments(...),
          body=[
            Return(
              value=Constant(value='hello')
            )
          ],
          decorator_list=[],
          returns=None
        )
      ]
    )
  ]
)
```

## pyxplod's AST Pipeline

### 1. File Parsing

```python
# src/pyxplod/ast_utils.py (simplified)
def parse_file(file_path: Path) -> ast.Module:
    """Parse a Python file into an AST."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return ast.parse(content, filename=str(file_path))
    except SyntaxError as e:
        logger.error(f"Syntax error in {file_path}: {e}")
        raise
```

### 2. Definition Discovery

pyxplod identifies top-level definitions to extract:

```python
def find_top_level_definitions(tree: ast.Module) -> list[ast.stmt]:
    """Find all top-level class and function definitions."""
    definitions = []
    for node in tree.body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            definitions.append(node)
    return definitions
```

**Extracted node types:**
- `ast.ClassDef`: Class definitions
- `ast.FunctionDef`: Function definitions  
- `ast.AsyncFunctionDef`: Async function definitions

### 3. Name Usage Analysis

For each definition, pyxplod analyzes what names (variables, functions, classes) it uses:

```python
class NameVisitor(ast.NodeVisitor):
    """Collect all names used within an AST node."""
    
    def __init__(self):
        self.names = set()
    
    def visit_Name(self, node: ast.Name):
        """Visit Name nodes (variable references)."""
        if isinstance(node.ctx, (ast.Load, ast.Del)):
            self.names.add(node.id)
        self.generic_visit(node)
    
    def visit_Attribute(self, node: ast.Attribute):
        """Visit Attribute nodes (e.g., module.function)."""
        if isinstance(node.value, ast.Name):
            self.names.add(node.value.id)
        self.generic_visit(node)
```

**Example analysis:**
```python
def process_data(filename: str) -> dict:
    """Function that uses os, json, Path."""
    path = Path(filename)           # Uses: Path
    if not os.path.exists(path):    # Uses: os
        return {}
    with open(path) as f:           # Uses: open (builtin)
        return json.load(f)         # Uses: json

# Detected names: {"Path", "os", "json", "open"}
```

### 4. Import Analysis

pyxplod analyzes import statements to understand dependencies:

```python
def extract_imports(tree: ast.Module) -> list[ast.stmt]:
    """Extract all import statements from module."""
    imports = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(node)
    return imports

def analyze_import(import_node: ast.stmt) -> dict:
    """Analyze an import statement."""
    if isinstance(import_node, ast.Import):
        # import os, sys
        return {
            'type': 'import',
            'modules': [alias.name for alias in import_node.names],
            'aliases': {alias.name: alias.asname for alias in import_node.names if alias.asname}
        }
    elif isinstance(import_node, ast.ImportFrom):
        # from pathlib import Path
        return {
            'type': 'from_import', 
            'module': import_node.module,
            'names': [alias.name for alias in import_node.names],
            'level': import_node.level  # For relative imports
        }
```

### 5. Import Filtering

Only necessary imports are included in extracted files:

```python
def filter_imports_for_definition(
    imports: list[ast.stmt], 
    used_names: set[str],
    module_vars: dict[str, ast.stmt]
) -> list[ast.stmt]:
    """Filter imports to only those needed by the definition."""
    needed_imports = []
    
    for import_node in imports:
        if is_import_needed(import_node, used_names, module_vars):
            needed_imports.append(import_node)
    
    return needed_imports

def is_import_needed(import_node: ast.stmt, used_names: set[str], module_vars: dict) -> bool:
    """Check if an import is needed based on used names."""
    if isinstance(import_node, ast.Import):
        # Check if any imported module is used
        for alias in import_node.names:
            name = alias.asname if alias.asname else alias.name
            if name in used_names:
                return True
    
    elif isinstance(import_node, ast.ImportFrom):
        # Check if any imported name is used
        for alias in import_node.names:
            name = alias.asname if alias.asname else alias.name
            if name in used_names:
                return True
    
    return False
```

## Advanced AST Manipulation

### Module Variable Handling

When a definition uses module-level variables, they must be included:

```python
# Original module
DATABASE_URL = "postgresql://..."
API_KEY = "secret123"

class DatabaseManager:
    def __init__(self):
        self.url = DATABASE_URL  # Uses module variable
        
def api_call():
    headers = {"Authorization": API_KEY}  # Uses module variable
```

**Variable detection:**
```python
def find_module_variables(tree: ast.Module) -> dict[str, ast.stmt]:
    """Find all module-level variable assignments."""
    variables = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    variables[target.id] = node
    return variables

def get_needed_variables(definition: ast.stmt, module_vars: dict) -> list[ast.stmt]:
    """Get module variables needed by a definition."""
    visitor = NameVisitor()
    visitor.visit(definition)
    
    needed_vars = []
    for var_name, var_node in module_vars.items():
        if var_name in visitor.names:
            needed_vars.append(var_node)
    
    return needed_vars
```

### Decorator Handling

pyxplod correctly handles decorators and their dependencies:

```python
from functools import wraps
from typing import Callable

def my_decorator(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator          # Decorator uses: my_decorator, wraps, Callable
def decorated_function():
    pass
```

**Decorator analysis:**
```python
def analyze_decorators(definition: ast.stmt) -> set[str]:
    """Analyze decorator usage in a definition."""
    decorator_names = set()
    
    if hasattr(definition, 'decorator_list'):
        for decorator in definition.decorator_list:
            visitor = NameVisitor()
            visitor.visit(decorator)
            decorator_names.update(visitor.names)
    
    return decorator_names
```

### Type Annotation Processing

Type hints are analyzed for import dependencies:

```python
from typing import List, Dict, Optional
from pathlib import Path

def process_files(
    files: List[Path],           # Uses: List, Path
    config: Dict[str, str],      # Uses: Dict
    output: Optional[Path] = None # Uses: Optional, Path
) -> Dict[str, List[str]]:       # Uses: Dict, List
    pass
```

**Type annotation analysis:**
```python
def analyze_type_annotations(definition: ast.FunctionDef) -> set[str]:
    """Extract names used in type annotations."""
    type_names = set()
    
    # Return type annotation
    if definition.returns:
        visitor = NameVisitor()
        visitor.visit(definition.returns)
        type_names.update(visitor.names)
    
    # Argument type annotations
    for arg in definition.args.args:
        if arg.annotation:
            visitor = NameVisitor()
            visitor.visit(arg.annotation)
            type_names.update(visitor.names)
    
    return type_names
```

## AST Reconstruction

### Creating New Modules

pyxplod creates new AST modules for extracted definitions:

```python
def create_extracted_module(
    definition: ast.stmt,
    imports: list[ast.stmt], 
    module_vars: list[ast.stmt]
) -> ast.Module:
    """Create a new module with definition and dependencies."""
    
    body = []
    
    # Add necessary imports
    body.extend(imports)
    
    # Add blank line after imports (using ast.Expr with empty string)
    if imports:
        body.append(ast.Expr(value=ast.Constant(value="")))
    
    # Add module variables
    body.extend(module_vars)
    
    # Add blank line before definition
    if module_vars:
        body.append(ast.Expr(value=ast.Constant(value="")))
    
    # Add the definition
    body.append(definition)
    
    return ast.Module(body=body, type_ignores=[])
```

### Modifying Original Modules

The original module is updated to import extracted definitions:

```python
def modify_original_module(
    tree: ast.Module,
    extracted_definitions: list[str],
    import_statements: list[ast.stmt]
) -> ast.Module:
    """Modify original module to import extracted definitions."""
    
    new_body = []
    
    # Keep existing imports
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            new_body.append(node)
    
    # Add new import statements for extracted definitions
    new_body.extend(import_statements)
    
    # Add remaining non-definition statements
    for node in tree.body:
        if not isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef,
                                ast.Import, ast.ImportFrom)):
            new_body.append(node)
    
    return ast.Module(body=new_body, type_ignores=[])
```

### Code Generation

Convert AST back to Python code:

```python
import ast

def ast_to_code(tree: ast.Module) -> str:
    """Convert AST back to Python source code."""
    try:
        return ast.unparse(tree)
    except AttributeError:
        # Python < 3.9 fallback
        import astor
        return astor.to_source(tree)
```

## Error Handling in AST Processing

### Syntax Error Recovery

```python
def safe_parse_file(file_path: Path) -> ast.Module | None:
    """Safely parse a file, returning None on syntax errors."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return ast.parse(content, filename=str(file_path))
    except SyntaxError as e:
        logger.error(f"Syntax error in {file_path}:{e.lineno}: {e.msg}")
        return None
    except UnicodeDecodeError as e:
        logger.error(f"Encoding error in {file_path}: {e}")
        return None
```

### AST Validation

```python
def validate_ast(tree: ast.Module) -> bool:
    """Validate that AST is well-formed."""
    try:
        # Try to compile the AST
        compile(tree, '<string>', 'exec')
        return True
    except (SyntaxError, ValueError) as e:
        logger.error(f"Invalid AST: {e}")
        return False
```

## Performance Optimizations

### AST Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def parse_and_cache(file_path: str) -> ast.Module:
    """Parse file with caching for repeated access."""
    return parse_file(Path(file_path))
```

### Visitor Optimization

```python
class OptimizedNameVisitor(ast.NodeVisitor):
    """Optimized visitor that stops early when possible."""
    
    def __init__(self, target_names: set[str]):
        self.target_names = target_names
        self.found_names = set()
        self.stop_early = False
    
    def visit_Name(self, node: ast.Name):
        if node.id in self.target_names:
            self.found_names.add(node.id)
            
        # Stop early if we found all targets
        if self.found_names == self.target_names:
            self.stop_early = True
            return
            
        self.generic_visit(node)
```

## Debugging AST Processing

### AST Visualization

```python
def print_ast_structure(node: ast.AST, indent: int = 0) -> None:
    """Print AST structure for debugging."""
    print("  " * indent + type(node).__name__)
    for field, value in ast.iter_fields(node):
        if isinstance(value, list):
            for item in value:
                if isinstance(item, ast.AST):
                    print_ast_structure(item, indent + 1)
        elif isinstance(value, ast.AST):
            print_ast_structure(value, indent + 1)
```

### Import Debugging

```bash
# Enable AST debugging
export PYXPLOD_DEBUG_AST=true
pyxplod ./src ./out --method files --verbose
```

## Common AST Patterns

### Pattern: Finding All Function Calls

```python
class FunctionCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.calls = []
    
    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            self.calls.append(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            # Handle method calls like obj.method()
            if isinstance(node.func.value, ast.Name):
                self.calls.append(f"{node.func.value.id}.{node.func.attr}")
        self.generic_visit(node)
```

### Pattern: Finding Variable Assignments

```python
class AssignmentVisitor(ast.NodeVisitor):
    def __init__(self):
        self.assignments = {}
    
    def visit_Assign(self, node: ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.assignments[target.id] = node.value
        self.generic_visit(node)
```

## Next Steps

Understanding AST processing helps you:

- **Debug explosion issues** by understanding how code is analyzed
- **Contribute to pyxplod** with knowledge of the internals
- **Extend functionality** for custom use cases
- **Optimize performance** for large codebases

Continue with:
- [File Organization](file-organization.md) - How AST processing results in organized output
- [API Reference](api-reference.md) - Programmatic access to AST utilities