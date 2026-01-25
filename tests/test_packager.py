"""
Tests for the NotebookPackager class.
"""

import zipfile
import pytest
from io import BytesIO

from src.converter.packager import NotebookPackager
from src.converter.models import ProcessedNotebook, NotebookStats, ExportOptions


def create_test_notebook(
    name: str = "test_notebook",
    code: str = "print('hello')",
    outputs: str = "hello",
    markdown: str = "# Test",
    images: list = None,
) -> ProcessedNotebook:
    """Helper to create a test ProcessedNotebook."""
    return ProcessedNotebook(
        name=name,
        code=code,
        outputs=outputs,
        markdown=markdown,
        images=images or [],
        stats=NotebookStats(
            code_cells=1,
            markdown_cells=1,
            images=len(images) if images else 0,
            code_lines=1,
        ),
        size="1.00 KB",
        original_size_bytes=1024,
    )


class TestNotebookPackager:
    """Tests for NotebookPackager."""
    
    def test_create_zip_single_notebook(self):
        """Test creating a ZIP with a single notebook."""
        notebook = create_test_notebook()
        packager = NotebookPackager()
        
        zip_buffer = packager.create_zip([notebook])
        
        # Verify it's a valid ZIP
        with zipfile.ZipFile(zip_buffer, "r") as zf:
            names = zf.namelist()
            assert "test_notebook/test_notebook.py" in names
            assert "test_notebook/test_notebook_outputs.txt" in names
            assert "test_notebook/test_notebook_documentation.md" in names
    
    def test_create_zip_multiple_notebooks(self):
        """Test creating a ZIP with multiple notebooks."""
        notebooks = [
            create_test_notebook(name="notebook1"),
            create_test_notebook(name="notebook2"),
        ]
        packager = NotebookPackager()
        
        zip_buffer = packager.create_zip(notebooks)
        
        with zipfile.ZipFile(zip_buffer, "r") as zf:
            names = zf.namelist()
            assert "notebook1/notebook1.py" in names
            assert "notebook2/notebook2.py" in names
    
    def test_create_zip_with_images(self):
        """Test creating a ZIP with images."""
        images = [
            ("image_1.png", b"fake_png_data"),
            ("image_2.png", b"fake_png_data_2"),
        ]
        notebook = create_test_notebook(images=images)
        packager = NotebookPackager()
        
        zip_buffer = packager.create_zip([notebook])
        
        with zipfile.ZipFile(zip_buffer, "r") as zf:
            names = zf.namelist()
            assert "test_notebook/test_notebook_image_1.png" in names
            assert "test_notebook/test_notebook_image_2.png" in names
    
    def test_create_zip_without_outputs(self):
        """Test creating a ZIP without outputs."""
        notebook = create_test_notebook()
        options = ExportOptions(include_outputs=False)
        packager = NotebookPackager(options)
        
        zip_buffer = packager.create_zip([notebook])
        
        with zipfile.ZipFile(zip_buffer, "r") as zf:
            names = zf.namelist()
            assert "test_notebook/test_notebook.py" in names
            assert "test_notebook/test_notebook_outputs.txt" not in names
    
    def test_create_zip_without_markdown(self):
        """Test creating a ZIP without markdown."""
        notebook = create_test_notebook()
        options = ExportOptions(include_markdown=False)
        packager = NotebookPackager(options)
        
        zip_buffer = packager.create_zip([notebook])
        
        with zipfile.ZipFile(zip_buffer, "r") as zf:
            names = zf.namelist()
            assert "test_notebook/test_notebook.py" in names
            assert "test_notebook/test_notebook_documentation.md" not in names
    
    def test_create_zip_without_images(self):
        """Test creating a ZIP without images."""
        images = [("image_1.png", b"fake_data")]
        notebook = create_test_notebook(images=images)
        options = ExportOptions(include_images=False)
        packager = NotebookPackager(options)
        
        zip_buffer = packager.create_zip([notebook])
        
        with zipfile.ZipFile(zip_buffer, "r") as zf:
            names = zf.namelist()
            assert "test_notebook/test_notebook_image_1.png" not in names
    
    def test_create_zip_encoding(self):
        """Test encoding in ZIP files."""
        notebook = create_test_notebook(code="print('héllo wörld')")
        options = ExportOptions(encoding="utf-8")
        packager = NotebookPackager(options)
        
        zip_buffer = packager.create_zip([notebook])
        
        with zipfile.ZipFile(zip_buffer, "r") as zf:
            content = zf.read("test_notebook/test_notebook.py")
            assert "héllo wörld" in content.decode("utf-8")
    
    def test_create_single_file_code(self):
        """Test creating a single code file."""
        notebook = create_test_notebook(code="x = 1\ny = 2")
        packager = NotebookPackager()
        
        buffer = packager.create_single_file(notebook, "code")
        content = buffer.read().decode("utf-8")
        
        assert "x = 1" in content
        assert "y = 2" in content
    
    def test_create_single_file_outputs(self):
        """Test creating a single outputs file."""
        notebook = create_test_notebook(outputs="Output 1\nOutput 2")
        packager = NotebookPackager()
        
        buffer = packager.create_single_file(notebook, "outputs")
        content = buffer.read().decode("utf-8")
        
        assert "Output 1" in content
        assert "Output 2" in content
    
    def test_create_single_file_markdown(self):
        """Test creating a single markdown file."""
        notebook = create_test_notebook(markdown="# Title\n## Subtitle")
        packager = NotebookPackager()
        
        buffer = packager.create_single_file(notebook, "markdown")
        content = buffer.read().decode("utf-8")
        
        assert "# Title" in content
        assert "## Subtitle" in content
    
    def test_create_single_file_invalid_type(self):
        """Test creating a single file with invalid type."""
        notebook = create_test_notebook()
        packager = NotebookPackager()
        
        with pytest.raises(ValueError, match="Unknown file type"):
            packager.create_single_file(notebook, "invalid")


class TestNotebookPackagerFilenames:
    """Tests for ZIP filename generation."""
    
    def test_get_zip_filename_single_notebook(self):
        """Test filename for single notebook."""
        notebook = create_test_notebook(name="my_notebook")
        packager = NotebookPackager()
        
        filename = packager.get_zip_filename([notebook])
        
        assert filename == "my_notebook_package.zip"
    
    def test_get_zip_filename_multiple_notebooks(self):
        """Test filename for multiple notebooks."""
        notebooks = [
            create_test_notebook(name="notebook1"),
            create_test_notebook(name="notebook2"),
        ]
        packager = NotebookPackager()
        
        filename = packager.get_zip_filename(notebooks)
        
        assert filename == "notebooks_package.zip"
    
    def test_get_zip_filename_custom_name(self):
        """Test custom filename."""
        notebook = create_test_notebook()
        options = ExportOptions(custom_zip_name="my_custom_export")
        packager = NotebookPackager(options)
        
        filename = packager.get_zip_filename([notebook])
        
        assert filename == "my_custom_export.zip"


class TestNotebookPackagerEmptyContent:
    """Tests for handling empty content."""
    
    def test_empty_code(self):
        """Test notebook with no code."""
        notebook = create_test_notebook(code="")
        packager = NotebookPackager()
        
        zip_buffer = packager.create_zip([notebook])
        
        with zipfile.ZipFile(zip_buffer, "r") as zf:
            names = zf.namelist()
            # Python file should not be included if code is empty
            assert "test_notebook/test_notebook.py" not in names
    
    def test_empty_outputs(self):
        """Test notebook with no outputs."""
        notebook = create_test_notebook(outputs="")
        packager = NotebookPackager()
        
        zip_buffer = packager.create_zip([notebook])
        
        with zipfile.ZipFile(zip_buffer, "r") as zf:
            names = zf.namelist()
            assert "test_notebook/test_notebook_outputs.txt" not in names
    
    def test_empty_markdown(self):
        """Test notebook with no markdown."""
        notebook = create_test_notebook(markdown="")
        packager = NotebookPackager()
        
        zip_buffer = packager.create_zip([notebook])
        
        with zipfile.ZipFile(zip_buffer, "r") as zf:
            names = zf.namelist()
            assert "test_notebook/test_notebook_documentation.md" not in names
