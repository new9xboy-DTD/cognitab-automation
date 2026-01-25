"""Tests for cognitab_automation package."""

import cognitab_automation


def test_version():
    """Test that the package has a version."""
    assert hasattr(cognitab_automation, "__version__")
    assert isinstance(cognitab_automation.__version__, str)
    assert cognitab_automation.__version__ == "0.1.0"


def test_author():
    """Test that the package has an author."""
    assert hasattr(cognitab_automation, "__author__")
    assert isinstance(cognitab_automation.__author__, str)


def test_license():
    """Test that the package has a license."""
    assert hasattr(cognitab_automation, "__license__")
    assert cognitab_automation.__license__ == "MIT"
