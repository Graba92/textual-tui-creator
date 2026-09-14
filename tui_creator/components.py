from typing import Dict, Any, Optional
from textual.widgets import (
    Button, Label, Input, Checkbox, Select, ProgressBar,
    LoadingIndicator, DataTable, Rule, Switch, Markdown,
    OptionList, Digits, Static, Tabs, Tab
)
from textual.containers import Vertical, Horizontal, Container
from textual.widget import Widget

COMPONENT_ICONS = {
    "Container": "📦",
    "Vertical": "↕️",
    "Horizontal": "↔️",
    "Label": "🔤",
    "Button": "🔘",
    "Input": "📝",
    "Checkbox": "☑️",
    "Switch": "🎛️",
    "Select": "🔽",
    "OptionList": "📑",
    "DataTable": "📊",
    "Markdown": "📄",
    "Digits": "🔢",
    "ProgressBar": "⏳",
    "LoadingIndicator": "⌛",
    "Rule": "➖",
    "Tabs": "🗂️",
    "Header": "🔝",
    "Footer": "🔚",
    "Static": "⏹️",
}

COMPONENT_REGISTRY = {
    "Container": {"props": {}, "container": True, "desc": "Allgemeiner Behälter"},
    "Vertical": {"props": {}, "container": True, "desc": "Vertikales Spaltenlayout"},
    "Horizontal": {"props": {}, "container": True, "desc": "Horizontales Zeilenlayout"},
    "Label": {"props": {"text": "Ein Text-Element"}, "container": False, "desc": "Einfacher Text"},
    "Button": {"props": {"label": "Klick mich", "variant": "primary"}, "container": False, "desc": "Klickbare Schaltfläche"},
    "Input": {"props": {"placeholder": "Eingabe hier...", "password": False}, "container": False, "desc": "Texteingabefeld"},
    "Checkbox": {"props": {"label": "Option aktivieren", "value": False}, "container": False, "desc": "Auswahlkästchen"},
    "Switch": {"props": {"value": False}, "container": False, "desc": "Kippschalter (Ein/Aus)"},
    "Select": {"props": {"options": "Option Alpha, Option Beta, Option Gamma"}, "container": False, "desc": "Dropdown-Menü"},
    "OptionList": {"props": {"options": "Eintrag 1, Eintrag 2, Eintrag 3"}, "container": False, "desc": "Scrollbare Optionsliste"},
    "DataTable": {"props": {"columns": "ID, Komponente, Status, Last", "zebra_stripes": True}, "container": False, "desc": "Datentabelle mit Spalten"},
    "Markdown": {"props": {"markdown_text": "### Dokumentation\n- Element A\n- Element B\n```bash\necho 'CachyOS'\n```"}, "container": False, "desc": "Formatierter Markdown-Text"},
    "Digits": {"props": {"value": "42:00"}, "container": False, "desc": "Große Ziffernanzeige (Uhr/Metrik)"},
    "Tabs": {"props": {"tabs": "Übersicht, Details, Konfiguration"}, "container": False, "desc": "Registerkartenleiste"},
    "ProgressBar": {"props": {"total": 100, "progress": 65}, "container": False, "desc": "Fortschrittsbalken"},
    "LoadingIndicator": {"props": {}, "container": False, "desc": "Ladeanimation"},
    "Rule": {"props": {"line_style": "solid"}, "container": False, "desc": "Horizontale Trennlinie"},
    "Static": {"props": {"content": "Statischer Inhaltsbereich"}, "container": False, "desc": "Generischer Text-/Panelblock"},
    "Header": {"props": {"show_clock": True}, "container": False, "desc": "Standard-Kopfzeile"},
    "Footer": {"props": {}, "container": False, "desc": "Standard-Fußzeile mit Hotkeys"}
}

def create_preview_widget(type_name: str, id_name: str, props: Dict[str, Any], classes: str) -> Widget:
    """Instanziiert ein echtes Textual-Widget für die Live-Vorschau."""
    try:
        w: Optional[Widget] = None
        if type_name == "Label":
            w = Label(props.get("text", "Text"))
        elif type_name == "Button":
            w = Button(props.get("label", "Button"), variant=props.get("variant", "primary"))
        elif type_name == "Input":
            w = Input(placeholder=props.get("placeholder", ""), password=props.get("password", False))
        elif type_name == "Checkbox":
            w = Checkbox(props.get("label", "Option"), value=props.get("value", False))
        elif type_name == "Switch":
            w = Switch(value=props.get("value", False))
        elif type_name == "Select":
            raw_opts = props.get("options", "")
            options = [opt.strip() for opt in raw_opts.split(",") if opt.strip()]
            w = Select.from_values(options) if options else Select([])
        elif type_name == "OptionList":
            raw_opts = props.get("options", "")
            opts = [opt.strip() for opt in raw_opts.split(",") if opt.strip()]
            w = OptionList(*opts) if opts else OptionList()
        elif type_name == "DataTable":
            table = DataTable(zebra_stripes=props.get("zebra_stripes", True))
            cols_str = props.get("columns", "ID, Name, Status")
            cols = [c.strip() for c in cols_str.split(",") if c.strip()]
            for c in cols:
                table.add_column(c)
            table.add_row("01", "Core Engine", "Aktiv", "OK")
            table.add_row("02", "Cache Layer", "Sync", "100%")
            table.add_row("03", "Worker Pool", "Bereit", "4/4")
            w = table
        elif type_name == "Markdown":
            md_text = props.get("markdown_text", "# Titel\n*Markdown Vorschau*")
            w = Markdown(md_text)
        elif type_name == "Digits":
            w = Digits(str(props.get("value", "12:34")))
        elif type_name == "Tabs":
            raw_tabs = props.get("tabs", "Tab 1, Tab 2")
            tabs = [t.strip() for t in raw_tabs.split(",") if t.strip()]
            w = Tabs(*tabs) if tabs else Tabs("Tab")
        elif type_name == "Static":
            w = Static(props.get("content", "Statischer Text"))
        elif type_name == "ProgressBar":
            tot = float(props.get("total", 100))
            prog = float(props.get("progress", 50))
            w = ProgressBar(total=tot)
            w.progress = prog
        elif type_name == "LoadingIndicator":
            w = LoadingIndicator()
        elif type_name == "Rule":
            line_style = props.get("line_style", "solid")
            w = Rule(line_style=line_style)
        elif type_name == "Header":
            w = Label("⚡ Kopfzeile (Simulation: Titel & Uhr)", classes="mock-header")
        elif type_name == "Footer":
            w = Label("⚡ Fußzeile (Simulation: Hotkey-Leiste)", classes="mock-footer")
        elif type_name == "Vertical":
            w = Vertical()
        elif type_name == "Horizontal":
            w = Horizontal()
        elif type_name == "Container":
            w = Container()
        else:
            w = Label(f"[Unbekannt: {type_name}]")
        
        if w:
            w.id = f"prev_{id_name}"
            if classes:
                w.add_class(*classes.split())
        return w
    except Exception as e:
        return Label(f"Fehler in Vorschau: {e}", classes="error-label")
