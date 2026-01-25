"""
Sidebar configuration and rendering.
"""

import streamlit as st

from ..converter.models import ExportOptions
from .. import __version__


def render_sidebar() -> ExportOptions:
    """
    Render the sidebar with all configuration options.
    
    Returns:
        ExportOptions configured by the user.
    """
    with st.sidebar:
        st.markdown("### Settings")
        
        st.markdown("#### Export Options")
        include_outputs = st.toggle(
            "Include outputs",
            value=True,
            help="Include cell execution outputs in the export"
        )
        include_images = st.toggle(
            "Include images",
            value=True,
            help="Extract and include images from cell outputs"
        )
        include_markdown = st.toggle(
            "Include markdown",
            value=True,
            help="Export markdown cells as a separate documentation file"
        )
        
        st.markdown("---")
        
        with st.expander("Advanced Options"):
            remove_magic = st.toggle(
                "Remove magic commands",
                value=False,
                help="Remove IPython magic commands (%, !) from the code"
            )
            add_cell_numbers = st.toggle(
                "Add cell numbers",
                value=False,
                help="Add comments marking cell numbers in the code"
            )
            custom_zip_name = st.text_input(
                "Custom ZIP name",
                value="",
                placeholder="Auto-generated if empty",
                help="Customize the name of the downloaded ZIP file"
            )
            encoding = st.selectbox(
                "Output encoding",
                options=["utf-8", "utf-16", "ascii", "latin-1"],
                index=0,
                help="Character encoding for output files"
            )
        
        st.markdown("---")
        
        st.markdown("### About")
        st.markdown(
            f"""
            **Notebook Converter** v{__version__}
            
            Converts Jupyter Notebooks into:
            - Python scripts
            - Output files
            - Markdown documentation
            - Extracted images
            
            All files are processed in-memory.
            """
        )
        
        st.markdown("---")
        
        st.markdown(
            """
            [Documentation](https://github.com/JuanLara18/notebook-converter)
            
            [Report an Issue](https://github.com/JuanLara18/notebook-converter/issues)
            """
        )
    
    return ExportOptions(
        include_outputs=include_outputs,
        include_images=include_images,
        include_markdown=include_markdown,
        remove_magic_commands=remove_magic,
        add_cell_numbers=add_cell_numbers,
        custom_zip_name=custom_zip_name if custom_zip_name else None,
        encoding=encoding,
    )
