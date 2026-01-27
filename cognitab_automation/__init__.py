"""
cognitab-automation: A Python library for automated clicking methods.

This library provides tools and utilities for automating click operations.
"""

__version__ = "0.1.0"
__author__ = "new9xboy"
__license__ = "MIT"

# Import main modules here when they are created
# from .clicker import AutoClicker
# from .utils import ClickUtils
from .adb import Device, get_devices
from .config import Config
from .match import Match
from .region import Region
from .point import Point

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "Device",
    "get_devices",
    "Config",
    "Match",
    "Region",
    "Point",
]
