"""
UI module - Streamlit components and styling.
"""

from .styles import apply_styles, THEME_CSS
from .components import (
    render_header,
    render_stats_card,
    render_stats_overview,
    render_file_preview,
    render_notebook_details,
    render_progress_bar,
    render_error_message,
    render_upload_section,
)
from .sidebar import render_sidebar

__all__ = [
    "apply_styles",
    "THEME_CSS",
    "render_header",
    "render_stats_card",
    "render_stats_overview",
    "render_file_preview",
    "render_notebook_details",
    "render_progress_bar",
    "render_error_message",
    "render_upload_section",
    "render_sidebar",
]
