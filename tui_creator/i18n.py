#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
tui_creator/i18n.py — Internationalization (i18n) Engine for Textual TUI-Creator.
Provides comprehensive German (de_DE) and English (en_US) translations with dynamic switching.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any

CONFIG_FILE = Path.home() / ".config" / "textual-tui-creator" / "config.json"

_STRINGS: Dict[str, Dict[str, str]] = {
    "de": {
        # General & Navigation
        "app_title": "TUI-CREATOR",
        "app_subtitle": "Visueller GUI/TUI-Builder für Python Textual",
        "btn_quit": "Beenden",
        "btn_cancel": "Abbrechen",
        "btn_confirm": "Bestätigen",
        "btn_save": "Speichern",
        "btn_back": "Zurück zur Übersicht",
        "btn_lang_toggle": "🌐 Sprache: DE (Taste: L)",
        "status_ready": "Bereit",
        "status_saved": "Projekt erfolgreich gespeichert.",
        "status_exported": "Python-Code exportiert nach: {path}",

        # Start Screen
        "start_title": "🎨 TEXTUAL TUI-CREATOR",
        "start_subtitle": "Erstelle moderne Terminal-Benutzeroberflächen visuell im Handumdrehen",
        "start_projects_title": "Bestehende Projekte:",
        "start_no_projects": "Keine Projekte vorhanden. Erstelle dein erstes TUI-Projekt!",
        "btn_new_project": "➕ Neues Projekt",
        "btn_open_project": "📂 Öffnen / Bearbeiten",
        "btn_delete_project": "🗑️ Löschen",
        "confirm_delete_title": "Projekt löschen",
        "confirm_delete_msg": "Möchtest du das Projekt '{name}' wirklich unwiderruflich löschen?",

        # New Project Dialog
        "new_proj_dialog_title": "⚡ Neues TUI-Projekt erstellen",
        "lbl_proj_name": "Projektname:",
        "lbl_choose_template": "Vorlage wählen:",
        "btn_create_proj": "Projekt erstellen",
        "template_blank": "Leeres Projekt (Blank Canvas)",
        "template_blank_desc": "Startet mit einem völlig leeren Layout für maximale Gestaltungsfreiheit.",
        "template_dashboard": "System-Dashboard",
        "template_dashboard_desc": "Klassisches Administrations-Layout mit Header, Sidebar und Datenbereich.",
        "template_form": "Eingabeformular & Dialog",
        "template_form_desc": "Strukturierte Eingabemaske mit Textfeldern, Auswahllisten und Buttons.",

        # Editor Screen
        "editor_panel_components": "📦 Komponenten-Bibliothek",
        "editor_panel_canvas": "🖥️ Visueller Canvas & Vorschau",
        "editor_panel_props": "⚙️ Eigenschaften (Properties)",
        "editor_panel_code": "🐍 Generierter Python Textual Code",
        "btn_add_component": "➕ Komponente hinzufügen",
        "btn_remove_component": "➖ Entfernen",
        "btn_export_code": "💾 Code exportieren (.py)",
        "btn_preview_run": "▶ Live-Vorschau testen",
        "lbl_selected_comp": "Ausgewählte Komponente: {name}",
        "lbl_no_selection": "Keine Komponente ausgewählt",
        "lbl_prop_id": "Widget ID",
        "lbl_prop_classes": "CSS-Klassen",
        "lbl_prop_text": "Beschriftung / Text",
        "lbl_prop_variant": "Button-Variante",
        "lbl_prop_placeholder": "Platzhalter-Text",

        # Component Categories & Names
        "cat_containers": "Container & Layouts",
        "cat_widgets": "Basis-Widgets",
        "cat_input": "Eingabe-Elemente",
        "comp_container": "Container (Allgemein)",
        "comp_vertical": "Vertikaler Container",
        "comp_horizontal": "Horizontaler Container",
        "comp_header": "Header (Kopfzeile mit Uhr)",
        "comp_footer": "Footer (Fußzeile mit Tasten)",
        "comp_label": "Label (Textanzeige)",
        "comp_button": "Button (Schaltfläche)",
        "comp_input": "Input (Einzeiliges Textfeld)",
        "comp_datatable": "DataTable (Datentabelle)",
        "comp_switch": "Switch (Kippschalter)",
        "comp_progressbar": "ProgressBar (Fortschrittsbalken)",

        # CLI
        "cli_lang_saved": "[OK] Sprache dauerhaft auf '{lang}' gesetzt.",
        "cli_help_desc": "TUI-Creator — Visueller GUI/TUI-Builder für Python Textual",
    },
    "en": {
        # General & Navigation
        "app_title": "TUI-CREATOR",
        "app_subtitle": "Visual GUI/TUI Builder for Python Textual",
        "btn_quit": "Quit",
        "btn_cancel": "Cancel",
        "btn_confirm": "Confirm",
        "btn_save": "Save",
        "btn_back": "Back to Overview",
        "btn_lang_toggle": "🌐 Language: EN (Key: L)",
        "status_ready": "Ready",
        "status_saved": "Project saved successfully.",
        "status_exported": "Python code exported to: {path}",

        # Start Screen
        "start_title": "🎨 TEXTUAL TUI-CREATOR",
        "start_subtitle": "Create modern terminal user interfaces visually in no time",
        "start_projects_title": "Existing Projects:",
        "start_no_projects": "No projects found. Create your first TUI project!",
        "btn_new_project": "➕ New Project",
        "btn_open_project": "📂 Open / Edit",
        "btn_delete_project": "🗑️ Delete",
        "confirm_delete_title": "Delete Project",
        "confirm_delete_msg": "Do you really want to permanently delete project '{name}'?",

        # New Project Dialog
        "new_proj_dialog_title": "⚡ Create New TUI Project",
        "lbl_proj_name": "Project Name:",
        "lbl_choose_template": "Select Template:",
        "btn_create_proj": "Create Project",
        "template_blank": "Blank Canvas",
        "template_blank_desc": "Start with a completely empty layout for maximum creative freedom.",
        "template_dashboard": "System Dashboard",
        "template_dashboard_desc": "Classic administration layout with header, sidebar, and data area.",
        "template_form": "Input Form & Dialog",
        "template_form_desc": "Structured input form with text inputs, select boxes, and action buttons.",

        # Editor Screen
        "editor_panel_components": "📦 Component Library",
        "editor_panel_canvas": "🖥️ Visual Canvas & Preview",
        "editor_panel_props": "⚙️ Properties",
        "editor_panel_code": "🐍 Generated Python Textual Code",
        "btn_add_component": "➕ Add Component",
        "btn_remove_component": "➖ Remove",
        "btn_export_code": "💾 Export Code (.py)",
        "btn_preview_run": "▶ Test Live Preview",
        "lbl_selected_comp": "Selected Component: {name}",
        "lbl_no_selection": "No component selected",
        "lbl_prop_id": "Widget ID",
        "lbl_prop_classes": "CSS Classes",
        "lbl_prop_text": "Label / Text",
        "lbl_prop_variant": "Button Variant",
        "lbl_prop_placeholder": "Placeholder Text",

        # Component Categories & Names
        "cat_containers": "Containers & Layouts",
        "cat_widgets": "Basic Widgets",
        "cat_input": "Input Elements",
        "comp_container": "Container (General)",
        "comp_vertical": "Vertical Container",
        "comp_horizontal": "Horizontal Container",
        "comp_header": "Header (Title & Clock)",
        "comp_footer": "Footer (Keybindings)",
        "comp_label": "Label (Text Display)",
        "comp_button": "Button (Clickable)",
        "comp_input": "Input (Single-line Text)",
        "comp_datatable": "DataTable (Data Grid)",
        "comp_switch": "Switch (Toggle)",
        "comp_progressbar": "ProgressBar",

        # CLI
        "cli_lang_saved": "[OK] Language permanently set to '{lang}'.",
        "cli_help_desc": "TUI-Creator — Visual GUI/TUI Builder for Python Textual",
    },
}

_current_lang = "de"


def load_configured_language() -> str:
    """Lädt die gespeicherte Sprache aus der Konfiguration."""
    global _current_lang
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                lang = data.get("language", "de")
                if lang in ("de", "en"):
                    _current_lang = lang
                    return lang
    except Exception:
        pass
    return _current_lang


def save_configured_language(lang: str) -> None:
    """Speichert die gewählte Sprache persistent."""
    try:
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        data = {}
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        data["language"] = lang
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass


def set_language(lang: str) -> None:
    """Setzt die aktive Sprache ('de' oder 'en')."""
    global _current_lang
    if lang.lower().startswith("en"):
        _current_lang = "en"
    else:
        _current_lang = "de"


def get_language() -> str:
    """Gibt den aktuellen Sprachcode ('de' oder 'en') zurück."""
    return _current_lang


def toggle_language() -> str:
    """Wechselt zwischen Deutsch und Englisch und speichert die Wahl."""
    global _current_lang
    _current_lang = "en" if _current_lang == "de" else "de"
    save_configured_language(_current_lang)
    return _current_lang


def t(key: str, **kwargs: Any) -> str:
    """Übersetzt einen Schlüssel in die aktive Sprache mit optionaler Formatierung."""
    lang_dict = _STRINGS.get(_current_lang, _STRINGS["en"])
    text = lang_dict.get(key)
    if text is None:
        text = _STRINGS["en"].get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text
