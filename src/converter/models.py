"""
Data models for notebook conversion.
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional


@dataclass
class NotebookStats:
    """Statistics about a processed notebook."""
    
    code_cells: int = 0
    markdown_cells: int = 0
    raw_cells: int = 0
    images: int = 0
    code_lines: int = 0
    
    def __add__(self, other: "NotebookStats") -> "NotebookStats":
        """Allow adding stats together for totals."""
        return NotebookStats(
            code_cells=self.code_cells + other.code_cells,
            markdown_cells=self.markdown_cells + other.markdown_cells,
            raw_cells=self.raw_cells + other.raw_cells,
            images=self.images + other.images,
            code_lines=self.code_lines + other.code_lines,
        )


@dataclass
class ProcessedNotebook:
    """Container for a processed notebook's content."""
    
    name: str
    code: str
    outputs: str
    markdown: str
    images: List[Tuple[str, bytes]] = field(default_factory=list)
    stats: NotebookStats = field(default_factory=NotebookStats)
    size: str = ""
    original_size_bytes: int = 0


@dataclass
class ExportOptions:
    """Options for notebook export."""
    
    include_outputs: bool = True
    include_images: bool = True
    include_markdown: bool = True
    remove_magic_commands: bool = False
    add_cell_numbers: bool = False
    custom_zip_name: Optional[str] = None
    encoding: str = "utf-8"


@dataclass
class ConversionError:
    """Represents an error during conversion."""
    
    filename: str
    error_type: str
    message: str
    
    def __str__(self) -> str:
        return f"[{self.error_type}] {self.filename}: {self.message}"
