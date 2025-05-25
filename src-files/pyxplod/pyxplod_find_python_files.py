from pathlib import Path


def find_python_files(directory: Path) -> list[Path]:
    """Recursively find all Python files in a directory."""
    python_files = []
    for file in directory.rglob("*.py"):
        if "__pycache__" not in str(file) and ".pyc" not in str(file):
            python_files.append(file)
    return sorted(python_files)
