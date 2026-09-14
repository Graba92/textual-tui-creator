import sys

def main():
    try:
        from tui_creator.app import TuiCreatorApp
    except ImportError as e:
        print("Fehler beim Starten des TUI-Creators.")
        print(f"Details: {e}")
        print("Bitte stelle sicher, dass du das Programm im Hauptverzeichnis mit 'python3 -m tui_creator' startest")
        print("und 'textual' installiert ist.")
        sys.exit(1)

    app = TuiCreatorApp()
    app.run()

if __name__ == "__main__":
    main()
