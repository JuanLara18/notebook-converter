"""
Helper utility functions.
"""

import re
from io import BytesIO
from typing import BinaryIO


def format_size(size_bytes: int) -> str:
    """
    Format a byte size into a human-readable string.

    Args:
        size_bytes: Size in bytes.

    Returns:
        Formatted string like "1.23 MB".
    """
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"


def get_file_size(file: BinaryIO | BytesIO) -> str:
    """
    Get the size of a file-like object as a formatted string.

    Args:
        file: File-like object with getvalue() method.

    Returns:
        Formatted size string.
    """
    try:
        size_bytes = len(file.getvalue())
        return format_size(size_bytes)
    except AttributeError:
        # Fallback for files without getvalue
        current_pos = file.tell()
        file.seek(0, 2)  # Seek to end
        size_bytes = file.tell()
        file.seek(current_pos)  # Restore position
        return format_size(size_bytes)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing invalid characters.

    Args:
        filename: Original filename.

    Returns:
        Sanitized filename safe for filesystem use.
    """
    # Remove or replace invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing whitespace and dots
    sanitized = sanitized.strip(' .')
    # Ensure filename is not empty
    if not sanitized:
        sanitized = "unnamed"
    return sanitized


def truncate_text(text: str, max_length: int = 1000, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.

    Args:
        text: Text to truncate.
        max_length: Maximum length.
        suffix: Suffix to add if truncated.

    Returns:
        Truncated text.
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def count_lines(text: str, exclude_empty: bool = True) -> int:
    """
    Count the number of lines in text.

    Args:
        text: Text to count lines in.
        exclude_empty: Whether to exclude empty lines.

    Returns:
        Number of lines.
    """
    lines = text.split("\n")
    if exclude_empty:
        lines = [line for line in lines if line.strip()]
    return len(lines)
