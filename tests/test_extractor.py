"""
Tests for the NotebookExtractor class.
"""

import json
import pytest
from io import BytesIO

from src.converter.extractor import NotebookExtractor
from src.converter.models import ExportOptions


def create_notebook_file(cells: list, metadata: dict = None) -> BytesIO:
    """Helper to create a notebook file-like object."""
    notebook = {
        "cells": cells,
        "metadata": metadata or {},
        "nbformat": 4,
        "nbformat_minor": 4,
    }
    content = json.dumps(notebook).encode("utf-8")
    return BytesIO(content)


class TestNotebookExtractor:
    """Tests for NotebookExtractor."""
    
    def test_extract_empty_notebook(self):
        """Test extracting an empty notebook."""
        notebook_file = create_notebook_file([])
        extractor = NotebookExtractor()
        
        result, error = extractor.extract(notebook_file, "empty.ipynb")
        
        assert error is None
        assert result is not None
        assert result.name == "empty"
        assert result.code == ""
        assert result.stats.code_cells == 0
        assert result.stats.markdown_cells == 0
    
    def test_extract_code_cells(self):
        """Test extracting code cells."""
        cells = [
            {
                "cell_type": "code",
                "source": ["print('Hello')\n", "x = 1"],
                "outputs": [],
            },
            {
                "cell_type": "code",
                "source": ["y = 2"],
                "outputs": [],
            },
        ]
        notebook_file = create_notebook_file(cells)
        extractor = NotebookExtractor()
        
        result, error = extractor.extract(notebook_file, "test.ipynb")
        
        assert error is None
        assert result is not None
        assert result.stats.code_cells == 2
        assert "print('Hello')" in result.code
        assert "x = 1" in result.code
        assert "y = 2" in result.code
    
    def test_extract_markdown_cells(self):
        """Test extracting markdown cells."""
        cells = [
            {
                "cell_type": "markdown",
                "source": ["# Title\n", "Some text"],
            },
            {
                "cell_type": "markdown",
                "source": ["## Subtitle"],
            },
        ]
        notebook_file = create_notebook_file(cells)
        extractor = NotebookExtractor()
        
        result, error = extractor.extract(notebook_file, "test.ipynb")
        
        assert error is None
        assert result is not None
        assert result.stats.markdown_cells == 2
        assert "# Title" in result.markdown
        assert "## Subtitle" in result.markdown
    
    def test_extract_stream_outputs(self):
        """Test extracting stream outputs."""
        cells = [
            {
                "cell_type": "code",
                "source": ["print('Hello')"],
                "outputs": [
                    {
                        "output_type": "stream",
                        "name": "stdout",
                        "text": ["Hello\n"],
                    }
                ],
            },
        ]
        notebook_file = create_notebook_file(cells)
        extractor = NotebookExtractor()
        
        result, error = extractor.extract(notebook_file, "test.ipynb")
        
        assert error is None
        assert result is not None
        assert "Hello" in result.outputs
    
    def test_extract_with_magic_commands_removal(self):
        """Test removing magic commands."""
        cells = [
            {
                "cell_type": "code",
                "source": ["%matplotlib inline\n", "import pandas as pd\n", "!pip install numpy"],
                "outputs": [],
            },
        ]
        notebook_file = create_notebook_file(cells)
        options = ExportOptions(remove_magic_commands=True)
        extractor = NotebookExtractor(options)
        
        result, error = extractor.extract(notebook_file, "test.ipynb")
        
        assert error is None
        assert result is not None
        assert "%matplotlib" not in result.code
        assert "!pip" not in result.code
        assert "import pandas" in result.code
    
    def test_extract_with_cell_numbers(self):
        """Test adding cell numbers."""
        cells = [
            {
                "cell_type": "code",
                "source": ["x = 1"],
                "outputs": [],
            },
            {
                "cell_type": "code",
                "source": ["y = 2"],
                "outputs": [],
            },
        ]
        notebook_file = create_notebook_file(cells)
        options = ExportOptions(add_cell_numbers=True)
        extractor = NotebookExtractor(options)
        
        result, error = extractor.extract(notebook_file, "test.ipynb")
        
        assert error is None
        assert result is not None
        assert "# --- Cell 1 ---" in result.code
        assert "# --- Cell 2 ---" in result.code
    
    def test_extract_invalid_json(self):
        """Test handling invalid JSON."""
        notebook_file = BytesIO(b"not valid json")
        extractor = NotebookExtractor()
        
        result, error = extractor.extract(notebook_file, "invalid.ipynb")
        
        assert result is None
        assert error is not None
        assert error.error_type == "JSONError"
        assert "invalid.ipynb" in str(error)
    
    def test_extract_missing_cells_key(self):
        """Test handling notebook without cells key."""
        notebook_file = BytesIO(json.dumps({"metadata": {}}).encode())
        extractor = NotebookExtractor()
        
        result, error = extractor.extract(notebook_file, "no_cells.ipynb")
        
        assert result is None
        assert error is not None
        assert error.error_type == "ValidationError"
    
    def test_extract_source_as_string(self):
        """Test handling source as string instead of list."""
        cells = [
            {
                "cell_type": "code",
                "source": "x = 1",  # String instead of list
                "outputs": [],
            },
        ]
        notebook_file = create_notebook_file(cells)
        extractor = NotebookExtractor()
        
        result, error = extractor.extract(notebook_file, "test.ipynb")
        
        assert error is None
        assert result is not None
        assert "x = 1" in result.code
    
    def test_extract_without_outputs(self):
        """Test extracting without including outputs."""
        cells = [
            {
                "cell_type": "code",
                "source": ["print('test')"],
                "outputs": [
                    {
                        "output_type": "stream",
                        "text": ["test\n"],
                    }
                ],
            },
        ]
        notebook_file = create_notebook_file(cells)
        options = ExportOptions(include_outputs=False)
        extractor = NotebookExtractor(options)
        
        result, error = extractor.extract(notebook_file, "test.ipynb")
        
        assert error is None
        assert result is not None
        assert result.outputs == ""
    
    def test_extract_without_markdown(self):
        """Test extracting without including markdown."""
        cells = [
            {
                "cell_type": "markdown",
                "source": ["# Title"],
            },
        ]
        notebook_file = create_notebook_file(cells)
        options = ExportOptions(include_markdown=False)
        extractor = NotebookExtractor(options)
        
        result, error = extractor.extract(notebook_file, "test.ipynb")
        
        assert error is None
        assert result is not None
        assert result.markdown == ""


class TestNotebookExtractorFormatSize:
    """Tests for the _format_size static method."""
    
    def test_format_bytes(self):
        """Test formatting bytes."""
        assert NotebookExtractor._format_size(500) == "500.00 B"
    
    def test_format_kilobytes(self):
        """Test formatting kilobytes."""
        assert NotebookExtractor._format_size(1024) == "1.00 KB"
        assert NotebookExtractor._format_size(2048) == "2.00 KB"
    
    def test_format_megabytes(self):
        """Test formatting megabytes."""
        assert NotebookExtractor._format_size(1024 * 1024) == "1.00 MB"
    
    def test_format_gigabytes(self):
        """Test formatting gigabytes."""
        assert NotebookExtractor._format_size(1024 * 1024 * 1024) == "1.00 GB"
