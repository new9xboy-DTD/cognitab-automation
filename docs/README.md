# Documentation

This directory contains the documentation for cognitab-automation.

## Contents

- `api.md` - API reference documentation
- `usage.md` - Usage guide and examples
- `contributing.md` - Contribution guidelines

## Building Documentation

If you decide to use Sphinx for documentation:

```bash
pip install sphinx sphinx-rtd-theme
sphinx-quickstart docs
make html
```

Or for MkDocs:

```bash
pip install mkdocs mkdocs-material
mkdocs serve
```
