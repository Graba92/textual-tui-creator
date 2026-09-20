import sys
import argparse
from pathlib import Path

from tui_creator.i18n import (
    t,
    set_language,
    load_configured_language,
    save_configured_language,
)


def main():
    load_configured_language()

    parser = argparse.ArgumentParser(
        prog="textual-tui-creator",
        description="🎨 Textual TUI-Creator — Visual GUI/TUI Builder for Python Textual"
    )
    parser.add_argument("--lang", choices=["de", "en"], help="Sprache wählen ('de' oder 'en') / Select language ('de' or 'en')")
    parser.add_argument("--version", action="version", version="Textual TUI-Creator 1.0.0")

    args = parser.parse_args()

    if args.lang:
        set_language(args.lang)
        save_configured_language(args.lang)

    try:
        from tui_creator.app import TuiCreatorApp
    except ImportError as e:
        print("Fehler beim Starten des TUI-Creators / Error launching TUI-Creator.")
        print(f"Details: {e}")
        print("Bitte stelle sicher, dass Textual installiert ist: pip install textual rich")
        sys.exit(1)

    app = TuiCreatorApp()
    app.run()


if __name__ == "__main__":
    main()
