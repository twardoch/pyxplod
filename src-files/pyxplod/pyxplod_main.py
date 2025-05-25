from pathlib import Path

from loguru import logger
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn


def main(input: str, output: str, method: str = "files", verbose: bool = False) -> None:
    """Explode a Python project by extracting classes and functions into separate files.

    Args:
        input: Path to the input directory containing Python files
        output: Path to the output directory where exploded files will be created
        method: Explosion method - 'files' (default) or 'dirs'
        verbose: Enable verbose logging for debugging
    """
    if method not in ["files", "dirs"]:
        logger.error(f"Invalid method '{method}'. Must be 'files' or 'dirs'.")
        return
    if verbose:
        logger.remove()
        logger.add(console.print, format="{time:HH:mm:ss} | {level} | {message}", level="DEBUG")
    else:
        logger.remove()
        logger.add(console.print, format="{message}", level="INFO")
    input_path = Path(input).resolve()
    output_path = Path(output).resolve()
    if not validate_paths(input_path, output_path):
        return
    python_files = find_python_files(input_path)
    if not python_files:
        logger.warning(f"No Python files found in {input_path}")
        return
    logger.info(f"Found {len(python_files)} Python files to process")
    output_path.mkdir(parents=True, exist_ok=True)
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        task = progress.add_task("Processing files...", total=len(python_files))
        for py_file in python_files:
            try:
                if method == "files":
                    process_python_file(py_file, output_path, input_path)
                else:
                    process_python_file_dirs(py_file, output_path, input_path)
                progress.update(task, advance=1)
            except Exception as e:
                logger.error(f"Failed to process {py_file}: {e}")
                if verbose:
                    logger.exception("Detailed error:")
    logger.info(f"✨ Successfully exploded {len(python_files)} files to {output_path} using method '{method}'")
