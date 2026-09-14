#!/usr/bin/env python3
"""
TUI-Creator — Visueller GUI/TUI-Builder für Textual
Einstiegspunkt für den direkten Aufruf.
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from tui_creator.__main__ import main

if __name__ == "__main__":
    main()