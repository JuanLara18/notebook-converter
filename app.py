"""
Notebook Converter - Main Application Entry Point

A professional Streamlit application to convert Jupyter Notebooks
into organized code packages.
"""

import streamlit as st
from typing import List

from src import __version__
from src.converter import NotebookExtractor, NotebookPackager, ExportOptions, NotebookStats
from src.converter.models import ProcessedNotebook
from src.ui.styles import apply_styles
from src.ui.components import (
    render_header,
    render_stats_overview,
    render_file_preview,
    render_notebook_details,
    render_error_message,
    render_upload_section,
)
from src.ui.sidebar import render_sidebar
from src.utils import format_size


def configure_page() -> None:
    """Configure the Streamlit page settings."""
    st.set_page_config(
        page_title="Notebook Converter",
        page_icon="N",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://github.com/JuanLara18/notebook-converter",
            "Report a bug": "https://github.com/JuanLara18/notebook-converter/issues",
            "About": f"Notebook Converter v{__version__}"
        }
    )


def initialize_session_state() -> None:
    """Initialize session state variables."""
    if "processed_notebooks" not in st.session_state:
        st.session_state.processed_notebooks: List[ProcessedNotebook] = []
    if "errors" not in st.session_state:
        st.session_state.errors: List[str] = []
    if "total_stats" not in st.session_state:
        st.session_state.total_stats = NotebookStats()
    if "total_size_bytes" not in st.session_state:
        st.session_state.total_size_bytes = 0


def process_notebooks(
    uploaded_files: List,
    options: ExportOptions
) -> None:
    """
    Process uploaded notebook files.
    
    Args:
        uploaded_files: List of uploaded file objects.
        options: Export options for processing.
    """
    st.session_state.processed_notebooks = []
    st.session_state.errors = []
    st.session_state.total_stats = NotebookStats()
    st.session_state.total_size_bytes = 0
    
    extractor = NotebookExtractor(options)
    
    progress_container = st.empty()
    status_container = st.empty()
    
    for idx, uploaded_file in enumerate(uploaded_files):
        progress_container.progress(
            (idx + 1) / len(uploaded_files),
            text=f"Processing {uploaded_file.name}..."
        )
        
        notebook, error = extractor.extract(uploaded_file, uploaded_file.name)
        
        if error:
            st.session_state.errors.append(str(error))
        elif notebook:
            st.session_state.processed_notebooks.append(notebook)
            st.session_state.total_stats = st.session_state.total_stats + notebook.stats
            st.session_state.total_size_bytes += notebook.original_size_bytes
    
    progress_container.empty()
    
    success_count = len(st.session_state.processed_notebooks)
    error_count = len(st.session_state.errors)
    
    if success_count > 0:
        status_container.success(f"Processed {success_count} notebook(s) successfully.")
    
    if error_count > 0:
        st.warning(f"{error_count} file(s) encountered errors during processing.")


def render_download_section(options: ExportOptions) -> None:
    """
    Render the download section with ZIP file.
    
    Args:
        options: Export options for packaging.
    """
    if not st.session_state.processed_notebooks:
        return
    
    packager = NotebookPackager(options)
    notebooks = st.session_state.processed_notebooks
    
    zip_buffer = packager.create_zip(notebooks)
    zip_filename = packager.get_zip_filename(notebooks)
    
    st.download_button(
        label="Download Package",
        data=zip_buffer.getvalue(),
        file_name=zip_filename,
        mime="application/zip",
        use_container_width=True,
    )


def render_results_section() -> None:
    """Render the results section with statistics and previews."""
    if not st.session_state.processed_notebooks:
        return
    
    notebooks = st.session_state.processed_notebooks
    
    st.markdown("---")
    
    total_size = format_size(st.session_state.total_size_bytes)
    render_stats_overview(
        st.session_state.total_stats,
        total_size,
        len(notebooks)
    )
    
    st.markdown("---")
    st.markdown("### Processed Files")
    
    for notebook in notebooks:
        with st.expander(notebook.name, expanded=False):
            render_notebook_details(notebook)
            st.markdown("**Preview**")
            render_file_preview(notebook)


def main() -> None:
    """Main application entry point."""
    configure_page()
    apply_styles()
    initialize_session_state()
    
    options = render_sidebar()
    
    render_header()
    
    # Single column layout
    uploaded_files = render_upload_section()
    
    if uploaded_files:
        if st.button("Process Files", use_container_width=True, type="primary"):
            with st.spinner("Processing..."):
                process_notebooks(uploaded_files, options)
        
        render_download_section(options)
    
    render_error_message(st.session_state.errors)
    render_results_section()


if __name__ == "__main__":
    main()
