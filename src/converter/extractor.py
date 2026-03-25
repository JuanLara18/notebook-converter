"""
Notebook content extraction logic.
"""

import base64
import json
import re
from typing import BinaryIO

from .models import ConversionError, ExportOptions, NotebookStats, ProcessedNotebook


class NotebookExtractor:
    """Extracts content from Jupyter Notebooks."""

    SUPPORTED_IMAGE_FORMATS = ["image/png", "image/jpeg", "image/jpg", "image/gif"]
    MAGIC_COMMAND_PATTERN = re.compile(r"^\s*[%!].*$", re.MULTILINE)

    def __init__(self, options: ExportOptions | None = None):
        """
        Initialize the extractor with options.

        Args:
            options: Export options for customizing extraction behavior.
        """
        self.options = options or ExportOptions()

    def extract(
        self,
        notebook_file: BinaryIO,
        filename: str
    ) -> tuple[ProcessedNotebook | None, ConversionError | None]:
        """
        Extract content from a notebook file.

        Args:
            notebook_file: File-like object containing the notebook.
            filename: Original filename for the notebook.

        Returns:
            Tuple of (ProcessedNotebook, None) on success, or (None, ConversionError) on failure.
        """
        try:
            notebook_file.seek(0, 2)
            file_size = notebook_file.tell()
            notebook_file.seek(0)

            try:
                notebook_data = json.load(notebook_file)
            except json.JSONDecodeError as e:
                return None, ConversionError(
                    filename=filename,
                    error_type="JSONError",
                    message=f"Invalid JSON format: {str(e)}"
                )

            if not isinstance(notebook_data, dict):
                return None, ConversionError(
                    filename=filename,
                    error_type="ValidationError",
                    message="Notebook must be a JSON object"
                )

            if "cells" not in notebook_data:
                return None, ConversionError(
                    filename=filename,
                    error_type="ValidationError",
                    message="Notebook missing 'cells' key - may not be a valid Jupyter notebook"
                )

            # Extract metadata
            metadata = notebook_data.get("metadata", {})
            kernel_info = metadata.get("kernelspec", {})
            language = kernel_info.get("language", "python")

            # Initialize containers
            code_parts: list[str] = []
            output_parts: list[str] = []
            markdown_parts: list[str] = []
            images: list[tuple[str, bytes]] = []

            stats = NotebookStats()
            image_counter = 1
            code_cell_number = 1

            # Clean filename
            base_name = re.sub(r"\.ipynb$", "", filename, flags=re.IGNORECASE)

            # Build markdown document header
            if self.options.include_markdown:
                markdown_parts.append(f"# {base_name}")
                markdown_parts.append("")
                markdown_parts.append(f"> Extracted from `{filename}`")
                markdown_parts.append("")
                markdown_parts.append("---")
                markdown_parts.append("")

            # Process cells in order
            for cell in notebook_data.get("cells", []):
                cell_type = cell.get("cell_type", "")
                source = self._get_cell_source(cell)

                if cell_type == "code":
                    stats.code_cells += 1

                    # Process code for .py file
                    code_content = source
                    if self.options.remove_magic_commands:
                        code_content = self._remove_magic_commands(code_content)

                    if self.options.add_cell_numbers:
                        code_parts.append(f"# --- Cell {code_cell_number} ---")

                    code_parts.append(code_content)
                    code_parts.append("")

                    # Add to markdown document
                    if self.options.include_markdown and code_content.strip():
                        markdown_parts.append(f"### Code Cell {code_cell_number}")
                        markdown_parts.append("")
                        markdown_parts.append(f"```{language}")
                        markdown_parts.append(code_content)
                        markdown_parts.append("```")
                        markdown_parts.append("")

                    # Process outputs
                    if self.options.include_outputs:
                        cell_outputs, new_images = self._extract_outputs(
                            cell.get("outputs", []),
                            image_counter
                        )
                        if cell_outputs:
                            output_parts.append(f"=== Cell {code_cell_number} Output ===")
                            output_parts.append(cell_outputs)
                            output_parts.append("")

                            # Add output to markdown
                            if self.options.include_markdown:
                                markdown_parts.append("**Output:**")
                                markdown_parts.append("")
                                markdown_parts.append("```")
                                # Truncate very long outputs in markdown
                                output_preview = cell_outputs[:2000]
                                if len(cell_outputs) > 2000:
                                    output_preview += "\n... (output truncated)"
                                markdown_parts.append(output_preview)
                                markdown_parts.append("```")
                                markdown_parts.append("")

                        if self.options.include_images:
                            # Add image references to markdown
                            for img_name, img_bytes in new_images:
                                images.append((img_name, img_bytes))
                                if self.options.include_markdown:
                                    markdown_parts.append(
                                        f"![{img_name}]({base_name}_{img_name})"
                                    )
                                    markdown_parts.append("")
                            image_counter += len(new_images)

                    code_cell_number += 1

                elif cell_type == "markdown":
                    stats.markdown_cells += 1
                    if self.options.include_markdown and source.strip():
                        markdown_parts.append(source)
                        markdown_parts.append("")

                elif cell_type == "raw":
                    stats.raw_cells += 1
                    if self.options.include_markdown and source.strip():
                        markdown_parts.append("```")
                        markdown_parts.append(source)
                        markdown_parts.append("```")
                        markdown_parts.append("")

            # Add footer to markdown
            if self.options.include_markdown:
                markdown_parts.append("---")
                markdown_parts.append("")
                markdown_parts.append(
                    f"*Generated by Notebook Converter | "
                    f"{stats.code_cells} code cells, "
                    f"{stats.markdown_cells} markdown cells, "
                    f"{len(images)} images*"
                )

            # Compile results
            code_str = "\n".join(code_parts).strip()
            outputs_str = "\n".join(output_parts).strip()
            markdown_str = "\n".join(markdown_parts).strip()

            stats.images = len(images)
            stats.code_lines = len([line for line in code_str.split("\n") if line.strip()])

            processed = ProcessedNotebook(
                name=base_name,
                code=code_str,
                outputs=outputs_str,
                markdown=markdown_str,
                images=images,
                stats=stats,
                size=self._format_size(file_size),
                original_size_bytes=file_size,
            )

            return processed, None

        except Exception as e:
            return None, ConversionError(
                filename=filename,
                error_type="UnexpectedError",
                message=str(e)
            )

    def _get_cell_source(self, cell: dict) -> str:
        """Extract source from a cell, handling both list and string formats."""
        source = cell.get("source", [])
        if isinstance(source, list):
            return "".join(source)
        return str(source)

    def _remove_magic_commands(self, code: str) -> str:
        """Remove IPython magic commands from code."""
        lines = code.split("\n")
        filtered = [line for line in lines if not self.MAGIC_COMMAND_PATTERN.match(line)]
        return "\n".join(filtered)

    def _extract_outputs(
        self,
        outputs: list[dict],
        image_counter: int
    ) -> tuple[str, list[tuple[str, bytes]]]:
        """
        Extract text outputs and images from cell outputs.

        Args:
            outputs: List of output dictionaries from the cell.
            image_counter: Current image counter for naming.

        Returns:
            Tuple of (text_output, list of (image_name, image_bytes))
        """
        text_parts: list[str] = []
        images: list[tuple[str, bytes]] = []
        current_image = image_counter

        for out in outputs:
            output_type = out.get("output_type", "")

            if output_type == "stream":
                text = out.get("text", [])
                if isinstance(text, list):
                    text_parts.append("".join(text))
                else:
                    text_parts.append(str(text))

            elif output_type == "error":
                traceback = out.get("traceback", [])
                if traceback:
                    clean_traceback = [self._remove_ansi(line) for line in traceback]
                    text_parts.append("\n".join(clean_traceback))

            elif output_type in ["display_data", "execute_result"]:
                data = out.get("data", {})

                if "text/plain" in data:
                    text = data["text/plain"]
                    if isinstance(text, list):
                        text_parts.append("".join(text))
                    else:
                        text_parts.append(str(text))

                for img_format in self.SUPPORTED_IMAGE_FORMATS:
                    if img_format in data:
                        try:
                            image_data = data[img_format]
                            if isinstance(image_data, list):
                                image_data = "".join(image_data)

                            image_bytes = base64.b64decode(image_data)
                            extension = img_format.split("/")[1]
                            img_name = f"image_{current_image}.{extension}"
                            images.append((img_name, image_bytes))
                            text_parts.append(f"[Image: {img_name}]")
                            current_image += 1
                        except Exception:
                            text_parts.append(f"[Failed to extract {img_format} image]")

        return "\n".join(text_parts), images

    def _remove_ansi(self, text: str) -> str:
        """Remove ANSI escape codes from text."""
        ansi_pattern = re.compile(r"\x1b\[[0-9;]*m")
        return ansi_pattern.sub("", text)

    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """Format file size in appropriate units."""
        for unit in ["B", "KB", "MB", "GB"]:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} TB"
