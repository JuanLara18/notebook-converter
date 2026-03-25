# Development

## Project Structure

```
Notebook-Converter/
├── app.py                    # Main Streamlit application
├── src/
│   ├── converter/            # Core conversion logic
│   │   ├── extractor.py      # Content extraction
│   │   ├── packager.py       # ZIP packaging
│   │   └── models.py         # Data models
│   ├── ui/                   # UI components
│   │   ├── components.py     # Reusable elements
│   │   ├── styles.py         # CSS styling
│   │   └── sidebar.py        # Configuration panel
│   └── utils/
│       └── helpers.py        # Utilities
├── tests/                    # Test suite
├── .streamlit/
│   └── config.toml           # Streamlit configuration
├── pyproject.toml            # Project configuration (Poetry)
└── requirements.txt          # Dependencies (pip)
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_extractor.py
```

## Code Quality

This project uses **Black** for formatting and **Ruff** for linting:

```bash
black .
ruff check . --fix
```

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on reporting bugs, submitting fixes, and proposing features.
