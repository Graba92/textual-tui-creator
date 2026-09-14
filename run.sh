#!/usr/bin/env bash
# ==============================================================================
# Textual TUI-Creator — Universal Launcher
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -d "$SCRIPT_DIR/venv" ] && [ -f "$SCRIPT_DIR/venv/bin/python3" ]; then
    exec "$SCRIPT_DIR/venv/bin/python3" "$SCRIPT_DIR/tui_creator.py" "$@"
elif [ -d "$SCRIPT_DIR/.venv" ] && [ -f "$SCRIPT_DIR/.venv/bin/python3" ]; then
    exec "$SCRIPT_DIR/.venv/bin/python3" "$SCRIPT_DIR/tui_creator.py" "$@"
else
    exec python3 "$SCRIPT_DIR/tui_creator.py" "$@"
fi
