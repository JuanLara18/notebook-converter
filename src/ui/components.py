"""
Reusable UI components for the application.
"""


import streamlit as st

from ..converter.models import NotebookStats, ProcessedNotebook


def render_header() -> None:
    """Render the main application header."""
    st.markdown(
        """
        <div class="app-header">
            <h1>Notebook Converter</h1>
            <p>Convert Jupyter Notebooks into organized code packages</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stats_card(label: str, value: str | int) -> None:
    """
    Render a statistics card.

    Args:
        label: The label for the statistic.
        value: The value to display.
    """
    st.metric(label=label, value=value)


def render_stats_overview(stats: NotebookStats, total_size: str, file_count: int) -> None:
    """
    Render an overview of all statistics.

    Args:
        stats: Combined notebook statistics.
        total_size: Total size string.
        file_count: Number of processed files.
    """
    st.markdown("### Summary")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Files", file_count)
    with col2:
        st.metric("Total Size", total_size)
    with col3:
        st.metric("Code Cells", stats.code_cells)
    with col4:
        st.metric("Lines of Code", stats.code_lines)

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.metric("Markdown Cells", stats.markdown_cells)
    with col6:
        st.metric("Images", stats.images)
    with col7:
        st.metric("Raw Cells", stats.raw_cells)
    with col8:
        pass  # Empty for balance


def render_file_preview(notebook: ProcessedNotebook) -> None:
    """
    Render a preview of the processed notebook content.

    Args:
        notebook: The processed notebook to preview.
    """
    tabs = st.tabs(["Code", "Outputs", "Markdown", "Images"])

    with tabs[0]:
        if notebook.code:
            st.code(
                notebook.code[:5000] + ("..." if len(notebook.code) > 5000 else ""),
                language="python"
            )
        else:
            st.info("No code cells found.")

    with tabs[1]:
        if notebook.outputs:
            st.text(notebook.outputs[:3000] + ("..." if len(notebook.outputs) > 3000 else ""))
        else:
            st.info("No outputs found.")

    with tabs[2]:
        if notebook.markdown:
            st.markdown(notebook.markdown[:3000] + ("..." if len(notebook.markdown) > 3000 else ""))
        else:
            st.info("No markdown cells found.")

    with tabs[3]:
        if notebook.images:
            st.write(f"{len(notebook.images)} image(s) extracted")
            for img_name, img_bytes in notebook.images[:5]:
                st.image(img_bytes, caption=img_name, use_container_width=True)
            if len(notebook.images) > 5:
                st.info(f"{len(notebook.images) - 5} additional images not shown.")
        else:
            st.info("No images found.")


def render_notebook_details(notebook: ProcessedNotebook) -> None:
    """
    Render detailed information about a single notebook.

    Args:
        notebook: The processed notebook.
    """
    stats = notebook.stats

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Size", notebook.size)
    with col2:
        st.metric("Code Cells", stats.code_cells)
    with col3:
        st.metric("Markdown", stats.markdown_cells)
    with col4:
        st.metric("Images", stats.images)
    with col5:
        st.metric("Lines", stats.code_lines)


def render_progress_bar(current: int, total: int, text: str = "Processing...") -> None:
    """
    Render a progress bar with text.

    Args:
        current: Current progress value.
        total: Total value.
        text: Text to display.
    """
    progress = current / total if total > 0 else 0
    st.progress(progress, text=f"{text} ({current}/{total})")


def render_error_message(errors: list[str]) -> None:
    """
    Render error messages in a formatted way.

    Args:
        errors: List of error messages.
    """
    if not errors:
        return

    with st.expander("Errors", expanded=True):
        for error in errors:
            st.error(error)


def render_upload_section() -> list | None:
    """
    Render the file upload section.

    Returns:
        List of uploaded files or None.
    """
    st.markdown("### Upload")

    uploaded_files = st.file_uploader(
        "Select .ipynb files",
        type=["ipynb"],
        accept_multiple_files=True,
        help="Upload one or more Jupyter Notebook files. All processing happens in-memory.",
        key="notebook_uploader"
    )

    return uploaded_files if uploaded_files else None
