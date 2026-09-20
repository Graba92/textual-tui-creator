"""
TUI-Creator - Ein visueller Editor für Textual-basierte Terminal-Interfaces.
"""

from .i18n import t, set_language, get_language, toggle_language, load_configured_language

__version__ = "1.0.0"

__all__ = [
    "t",
    "set_language",
    "get_language",
    "toggle_language",
    "load_configured_language",
    "__version__",
]
