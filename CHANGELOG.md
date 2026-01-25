# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-01-25

### Added

- **Modular Architecture**: Reorganized codebase into `src/converter`, `src/ui`, and `src/utils` modules
- **Type Hints**: Full type annotations throughout the codebase
- **Dataclasses**: Introduced `NotebookStats`, `ProcessedNotebook`, `ExportOptions`, and `ConversionError` models
- **Enhanced Markdown Export**: Generate complete documentation that preserves notebook structure
  - Includes original markdown cells
  - Code cells with syntax highlighting
  - Cell outputs inline
  - Image references
  - Header and footer with metadata
- **Advanced Options**:
  - Remove IPython magic commands (`%` and `!` lines)
  - Add cell number comments to code
  - Custom ZIP filename
  - Multiple encoding options (UTF-8, UTF-16, ASCII, Latin-1)
- **Image Support**: Extended support for JPEG and GIF images in addition to PNG
- **Error Handling**: Robust error handling with clear error messages for malformed notebooks
- **Preview Tabs**: View code, outputs, markdown, and images in separate tabs before downloading
- **Modern UI**: 
  - Clean, professional design
  - Single-column layout for better readability
  - Progress bar during processing
  - Dark mode support
- **Testing**: Comprehensive test suite with pytest
- **Code Quality**: Poetry support, Ruff linting, Black formatting
- **Streamlit Configuration**: Custom theme in `.streamlit/config.toml`

### Changed

- **Python Requirement**: Minimum version is now 3.10 (was 3.9)
- **UI**: Removed emojis for a more professional appearance
- **Layout**: Changed from two-column to single-column layout
- **Entry Point**: Simplified `app.py` to use modular components
- **File Structure**: Each notebook gets its own folder in the ZIP

### Fixed

- Better handling of notebooks where `source` is a string instead of a list
- Proper ANSI escape code removal from error tracebacks
- File size calculation for large files

## [1.0.0] - Initial Release

### Added

- Basic notebook conversion functionality
- Code extraction to Python files
- Output extraction to text files
- Image extraction (PNG only)
- Multiple file upload support
- Basic statistics display
- ZIP download functionality

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-01-25 | Major refactor with modular architecture, enhanced markdown export, professional UI |
| 1.0.0 | - | Initial release |
