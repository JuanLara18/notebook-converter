"""
Centralized CSS styles for the application.
"""

import streamlit as st

THEME_CSS = """
<style>
/* Main container */
.main {
    padding: 1rem 2rem;
}

/* Header styling */
.app-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    color: white;
    text-align: center;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.app-header h1 {
    margin: 0;
    font-size: 2.2rem;
    font-weight: 700;
    letter-spacing: -0.5px;
}

.app-header p {
    margin: 0.5rem 0 0 0;
    opacity: 0.9;
    font-size: 1rem;
}

/* Card styling */
.stat-card {
    background: var(--background-secondary);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 0.5rem 0;
    border: 1px solid rgba(128, 128, 128, 0.2);
    transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

/* Upload section */
.upload-section {
    border: 2px dashed #667eea;
    border-radius: 12px;
    padding: 2rem;
    margin: 1rem 0;
    text-align: center;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
    transition: border-color 0.3s, background 0.3s;
}

.upload-section:hover {
    border-color: #764ba2;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
}

/* Button styling */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    border: none;
    font-weight: 600;
    font-size: 1rem;
    transition: transform 0.2s, box-shadow 0.2s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.stButton > button:active {
    transform: translateY(0);
}

/* Download button */
.stDownloadButton > button {
    width: 100%;
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    border: none;
    font-weight: 600;
    font-size: 1rem;
    transition: transform 0.2s, box-shadow 0.2s;
}

.stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(17, 153, 142, 0.4);
}

/* Expander styling */
.streamlit-expanderHeader {
    background: var(--background-secondary);
    border-radius: 8px;
    font-weight: 600;
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    background: var(--background-secondary);
    border-radius: 8px 8px 0 0;
    padding: 0.75rem 1.5rem;
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

/* Progress bar */
.stProgress > div > div > div > div {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: var(--background-secondary);
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}

/* Metrics */
[data-testid="stMetricValue"] {
    font-size: 1.5rem;
    font-weight: 700;
}

[data-testid="stMetricLabel"] {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
</style>
"""


def apply_styles() -> None:
    """Apply the theme CSS to the Streamlit app."""
    st.markdown(THEME_CSS, unsafe_allow_html=True)


def render_custom_header(title: str, subtitle: str) -> None:
    """
    Render a custom styled header.

    Args:
        title: Main title text.
        subtitle: Subtitle text.
    """
    st.markdown(
        f"""
        <div class="app-header">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
