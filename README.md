[🇩🇪 Zur deutschen Dokumentation wechseln](README_DE.md) | [🇬🇧 Switch to English Documentation](README.md)

# 🛠️ Textual TUI-Creator

[![GitHub](https://img.shields.io/badge/GitHub-Graba92%2Ftextual--tui--creator-blue?logo=github)](https://github.com/Graba92/textual-tui-creator)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-blue.svg)](https://python.org)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python)](https://python.org)
[![Framework](https://img.shields.io/badge/Framework-Textual-green.svg)](https://textual.textualize.io)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

<p align="center">
  <img src="preview_editor.png" alt="Textual TUI-Creator Visual Designer" width="900">
</p>
<p align="center">
  <img src="preview_projects.png" alt="Textual TUI-Creator Projects Overview" width="900">
</p>

**Textual TUI-Creator** is an interactive, visual WYSIWYG editor and code generator for [Textual](https://textual.textualize.io/)-based Terminal User Interfaces (TUIs) in Python.

It enables developers and system architects to design complex hierarchical terminal layouts interactively—complete with real-time preview, live property inspector, and direct export into clean, standalone Python source code.

---

## ✨ Features

- 🏗️ **Visual Layout Editor**: Interactively build hierarchical tree layouts (`Vertical`, `Horizontal`, `Container`).
- 🧩 **Extensive Widget Library**:
  - `Label`, `Button` (Primary, Success, Warning, Error variants)
  - `Input` (placeholders, password masking)
  - `Checkbox`, `Select` dropdown menus
  - `ProgressBar`, `LoadingIndicator`
  - `Rule` (Horizontal dividers), `Header`, `Footer`
- ⚡ **Real-Time Live Preview**: Instantly preview widgets and layout flow directly in the terminal as you design.
- 🔍 **Property Inspector**: Customize IDs, CSS classes, widget-specific parameters, and event hooks.
- 🐍 **Autonomous Python Code Generation**: Export standard, production-ready Textual application code (`app.py`) with zero editor dependencies.
- 💾 **Project Persistence & History**:
  - Automatic saving and loading of JSON project files located at `~/.local/share/tui-creator/projects/`.
  - Full Undo/Redo support (`Ctrl+Z` / `Ctrl+Y`).

---

## 🏛️ Project Architecture

```text
textual-tui-creator/
├── tui_creator.py              # Direct launcher script
├── start_tui_creator.sh        # Shell launcher script
├── run.sh                      # Universal runner (auto-detects virtualenv)
├── setup.sh                    # Automated setup and installer
├── requirements.txt            # Python dependencies
├── README.md                   # English documentation (this file)
├── README_DE.md                # German documentation
├── .gitignore                  # Git ignore rules
│
└── tui_creator/                # Python package
    ├── __init__.py             # Package initializer
    ├── __main__.py             # Package entrypoint
    ├── app.py                  # Textual application instance & routing
    ├── components.py           # Component library and widget descriptors
    ├── generator.py            # Python Textual source code generator
    ├── models.py               # Data models for layout nodes and schema
    ├── storage.py              # JSON project storage and project management
    └── ui.py                   # Editor views, component tree and inspector
```

---

## 🚀 Installation & Setup

### 1. Automated Setup (Recommended)

```bash
git clone https://github.com/Graba92/textual-tui-creator.git
cd textual-tui-creator
chmod +x setup.sh run.sh
./setup.sh
```

### 2. Native Pacman Installation (Arch Linux / CachyOS)

```bash
sudo pacman -S --needed python-textual
```

### 3. Manual Virtual Environment Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🖥️ Usage

### Launch the Editor
```bash
./run.sh
# or launch with explicit language
python3 tui_creator.py --lang en
python3 tui_creator.py --lang de
```

### ⌨️ Keybindings

| Shortcut | Action |
| :---: | :--- |
| `L` | Toggle language between **English** and **Deutsch** |
| `Ctrl + S` | Save current project |
| `Ctrl + Z` | Undo last operation |
| `Ctrl + Y` | Redo last operation |
| `Ctrl + E` | Export code to `.py` file |
| `F1` | Display help & shortcuts modal |
| `Esc` | Return to project home / overview |
| `Tab` / `Shift+Tab` | Cycle focus between tree, preview, and inspector |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
