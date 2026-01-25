"""
Packaging logic for creating ZIP archives.
"""

import zipfile
from io import BytesIO
from typing import List, Optional

from .models import ProcessedNotebook, ExportOptions


class NotebookPackager:
    """Creates ZIP packages from processed notebooks."""
    
    def __init__(self, options: Optional[ExportOptions] = None):
        """
        Initialize the packager with options.
        
        Args:
            options: Export options for customizing package contents.
        """
        self.options = options or ExportOptions()
    
    def create_zip(
        self, 
        notebooks: List[ProcessedNotebook],
        zip_name: Optional[str] = None
    ) -> BytesIO:
        """
        Create a ZIP file containing all processed notebooks.
        
        Args:
            notebooks: List of processed notebooks to package.
            zip_name: Optional custom name for the zip (without extension).
            
        Returns:
            BytesIO buffer containing the ZIP file.
        """
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for notebook in notebooks:
                self._add_notebook_to_zip(zip_file, notebook)
        
        zip_buffer.seek(0)
        return zip_buffer
    
    def _add_notebook_to_zip(
        self, 
        zip_file: zipfile.ZipFile, 
        notebook: ProcessedNotebook
    ) -> None:
        """
        Add a single notebook's files to the ZIP archive.
        
        Args:
            zip_file: ZipFile object to write to.
            notebook: Processed notebook to add.
        """
        base_name = notebook.name
        folder = f"{base_name}/"
        
        # Add Python file (always included)
        if notebook.code:
            zip_file.writestr(
                f"{folder}{base_name}.py",
                notebook.code.encode(self.options.encoding)
            )
        
        # Add outputs file
        if self.options.include_outputs and notebook.outputs:
            zip_file.writestr(
                f"{folder}{base_name}_outputs.txt",
                notebook.outputs.encode(self.options.encoding)
            )
        
        # Add markdown file
        if self.options.include_markdown and notebook.markdown:
            zip_file.writestr(
                f"{folder}{base_name}_documentation.md",
                notebook.markdown.encode(self.options.encoding)
            )
        
        # Add images
        if self.options.include_images and notebook.images:
            for img_name, img_content in notebook.images:
                zip_file.writestr(
                    f"{folder}{base_name}_{img_name}",
                    img_content
                )
    
    def create_single_file(
        self, 
        notebook: ProcessedNotebook, 
        file_type: str = "code"
    ) -> BytesIO:
        """
        Create a single file from a notebook.
        
        Args:
            notebook: Processed notebook.
            file_type: Type of file to create ("code", "outputs", "markdown").
            
        Returns:
            BytesIO buffer containing the file.
        """
        buffer = BytesIO()
        
        if file_type == "code":
            content = notebook.code
        elif file_type == "outputs":
            content = notebook.outputs
        elif file_type == "markdown":
            content = notebook.markdown
        else:
            raise ValueError(f"Unknown file type: {file_type}")
        
        buffer.write(content.encode(self.options.encoding))
        buffer.seek(0)
        return buffer
    
    def get_zip_filename(self, notebooks: List[ProcessedNotebook]) -> str:
        """
        Generate an appropriate filename for the ZIP.
        
        Args:
            notebooks: List of notebooks being packaged.
            
        Returns:
            Suggested filename for the ZIP.
        """
        if self.options.custom_zip_name:
            return f"{self.options.custom_zip_name}.zip"
        
        if len(notebooks) == 1:
            return f"{notebooks[0].name}_package.zip"
        
        return "notebooks_package.zip"
