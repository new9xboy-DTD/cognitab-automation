# cognitab-automation

A Python library for automated clicking methods and GUI automation.

## Installation

### From Source

```bash
git clone https://github.com/new9xboy-DTD/cognitab-automation.git
cd cognitab-automation
pip install -e .
```

### From PyPI (once published)

```bash
pip install cognitab-automation
```

## Usage

```python
import cognitab_automation

# Your automation code here
# Example usage will be added as the library develops
```

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/new9xboy-DTD/cognitab-automation.git
cd cognitab-automation
```

2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

3. Run tests:
```bash
pytest
```

4. Run linting:
```bash
black cognitab_automation tests
flake8 cognitab_automation tests
```

## Project Structure

```
cognitab-automation/
├── cognitab_automation/     # Main package directory
│   └── __init__.py          # Package initialization
├── tests/                   # Test directory
│   ├── __init__.py
│   └── test_package.py      # Package tests
├── docs/                    # Documentation
├── examples/                # Usage examples
├── setup.py                 # Setup script for pip
├── pyproject.toml           # Modern Python project configuration
├── requirements.txt         # Package dependencies
├── .gitignore              # Git ignore file
├── LICENSE                  # MIT License
└── README.md               # This file
```

## Features (Planned)

- Auto-click functionality
- GUI automation utilities
- Click pattern recording and playback
- Cross-platform support

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

new9xboy

## Changelog

### Version 0.1.0 (Initial Release)
- Initial project structure
- Basic package setup
