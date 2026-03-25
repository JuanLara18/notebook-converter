"""
Tests for data models.
"""


from src.converter.models import (
    ConversionError,
    ExportOptions,
    NotebookStats,
    ProcessedNotebook,
)


class TestNotebookStats:
    """Tests for NotebookStats dataclass."""

    def test_default_values(self):
        """Test default values are zero."""
        stats = NotebookStats()

        assert stats.code_cells == 0
        assert stats.markdown_cells == 0
        assert stats.raw_cells == 0
        assert stats.images == 0
        assert stats.code_lines == 0

    def test_custom_values(self):
        """Test creating with custom values."""
        stats = NotebookStats(
            code_cells=5,
            markdown_cells=3,
            raw_cells=1,
            images=2,
            code_lines=100,
        )

        assert stats.code_cells == 5
        assert stats.markdown_cells == 3
        assert stats.raw_cells == 1
        assert stats.images == 2
        assert stats.code_lines == 100

    def test_addition(self):
        """Test adding two NotebookStats together."""
        stats1 = NotebookStats(code_cells=5, markdown_cells=3, images=2, code_lines=100)
        stats2 = NotebookStats(code_cells=3, markdown_cells=2, images=1, code_lines=50)

        combined = stats1 + stats2

        assert combined.code_cells == 8
        assert combined.markdown_cells == 5
        assert combined.images == 3
        assert combined.code_lines == 150

    def test_addition_preserves_original(self):
        """Test that addition doesn't modify original objects."""
        stats1 = NotebookStats(code_cells=5)
        stats2 = NotebookStats(code_cells=3)

        _ = stats1 + stats2

        assert stats1.code_cells == 5
        assert stats2.code_cells == 3


class TestProcessedNotebook:
    """Tests for ProcessedNotebook dataclass."""

    def test_required_fields(self):
        """Test creating with required fields."""
        notebook = ProcessedNotebook(
            name="test",
            code="print('hello')",
            outputs="hello",
            markdown="# Test",
        )

        assert notebook.name == "test"
        assert notebook.code == "print('hello')"
        assert notebook.outputs == "hello"
        assert notebook.markdown == "# Test"

    def test_default_values(self):
        """Test default values for optional fields."""
        notebook = ProcessedNotebook(
            name="test",
            code="",
            outputs="",
            markdown="",
        )

        assert notebook.images == []
        assert notebook.stats.code_cells == 0
        assert notebook.size == ""
        assert notebook.original_size_bytes == 0

    def test_with_images(self):
        """Test creating with images."""
        images = [("image1.png", b"data1"), ("image2.png", b"data2")]
        notebook = ProcessedNotebook(
            name="test",
            code="",
            outputs="",
            markdown="",
            images=images,
        )

        assert len(notebook.images) == 2
        assert notebook.images[0][0] == "image1.png"


class TestExportOptions:
    """Tests for ExportOptions dataclass."""

    def test_default_values(self):
        """Test default export options."""
        options = ExportOptions()

        assert options.include_outputs is True
        assert options.include_images is True
        assert options.include_markdown is True
        assert options.remove_magic_commands is False
        assert options.add_cell_numbers is False
        assert options.custom_zip_name is None
        assert options.encoding == "utf-8"

    def test_custom_values(self):
        """Test creating with custom values."""
        options = ExportOptions(
            include_outputs=False,
            include_images=False,
            remove_magic_commands=True,
            custom_zip_name="my_export",
            encoding="latin-1",
        )

        assert options.include_outputs is False
        assert options.include_images is False
        assert options.remove_magic_commands is True
        assert options.custom_zip_name == "my_export"
        assert options.encoding == "latin-1"


class TestConversionError:
    """Tests for ConversionError dataclass."""

    def test_creation(self):
        """Test creating a ConversionError."""
        error = ConversionError(
            filename="test.ipynb",
            error_type="JSONError",
            message="Invalid JSON format",
        )

        assert error.filename == "test.ipynb"
        assert error.error_type == "JSONError"
        assert error.message == "Invalid JSON format"

    def test_str_representation(self):
        """Test string representation."""
        error = ConversionError(
            filename="test.ipynb",
            error_type="JSONError",
            message="Invalid JSON format",
        )

        str_repr = str(error)

        assert "[JSONError]" in str_repr
        assert "test.ipynb" in str_repr
        assert "Invalid JSON format" in str_repr
