# pyxplod: Python Code Exploder

Welcome to the comprehensive documentation for **pyxplod**, a powerful command-line tool designed to refactor Python codebases by "exploding" them into modular components.

## Table of Contents & TLDR

### 🚀 [Installation & Setup](installation.md)
**TLDR**: Install with `uv pip install pyxplod` or from source. Requires Python 3.9+.

### ⚡ [Quick Start Guide](quickstart.md) 
**TLDR**: Run `pyxplod input_dir output_dir --method files` to extract classes/functions into separate files.

### 🧠 [Understanding Explosion](concepts.md)
**TLDR**: pyxplod parses Python AST to extract top-level definitions, creating self-contained modules with filtered imports.

### 🛠️ [Methods & Strategies](methods.md)
**TLDR**: Two methods - `files` (extract to sibling files) and `dirs` (extract to subdirectories with `__init__.py`).

### 💻 [Command Line Usage](cli-usage.md)
**TLDR**: Full CLI reference with examples, arguments, and common usage patterns.

### ⚙️ [Configuration Options](configuration.md)
**TLDR**: Customize behavior with verbose logging, output patterns, and method-specific options.

### 🔬 [AST Processing](ast-processing.md)
**TLDR**: Deep dive into how pyxplod analyzes Python code structure and handles dependencies.

### 📁 [File Organization](file-organization.md)
**TLDR**: Learn output patterns, naming conventions, and directory structures for both methods.

### 📚 [API Reference](api-reference.md)
**TLDR**: Complete function and class documentation for programmatic usage.

---

## What is pyxplod?

`pyxplod` is a command-line tool that automatically refactors Python codebases by extracting top-level classes and functions into their own separate files. The original files are then updated to import these extracted components, creating a more modular and maintainable code structure.

### Key Features

- **🔧 Automated Refactoring**: Extract classes and functions without manual intervention
- **📦 Modular Output**: Choose between file-based or directory-based organization  
- **🎯 Smart Imports**: Automatically manages import statements and dependencies
- **🔍 AST-Based**: Uses Python's Abstract Syntax Tree for precise code analysis
- **⚡ Fast Processing**: Efficiently handles large codebases
- **🛡️ Safe Operation**: Preserves original code structure and functionality

### Who Should Use pyxplod?

- **Developers** working on large Python projects seeking better organization
- **Software Engineers** refactoring legacy codebases  
- **Teams** aiming to improve code modularity and maintainability
- **Educators** demonstrating Python project structure concepts

### Quick Example

Transform a monolithic Python file:

```python
# utils.py (before)
class DataProcessor:
    def process(self): pass

def helper_function():
    return "helper"

CONSTANT = 42
```

Into a modular structure:

```python
# utils.py (after - files method)
from .utils_data_processor import DataProcessor  
from .utils_helper_function import helper_function

CONSTANT = 42
```

```python
# utils_data_processor.py (new file)
class DataProcessor:
    def process(self): pass
```

```python  
# utils_helper_function.py (new file)
def helper_function():
    return "helper"
```

---

Ready to get started? Begin with our [Installation & Setup](installation.md) guide!