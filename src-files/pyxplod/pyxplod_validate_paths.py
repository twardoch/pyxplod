from pathlib import Path

from loguru import logger


def validate_paths(input_path: Path, output_path: Path) -> bool:
    """Validate input and output paths."""
    if not input_path.exists():
        logger.error(f"Input path does not exist: {input_path}")
        return False
    if not input_path.is_dir():
        logger.error(f"Input path is not a directory: {input_path}")
        return False
    if output_path.exists() and (not output_path.is_dir()):
        logger.error(f"Output path exists but is not a directory: {output_path}")
        return False
    return True
