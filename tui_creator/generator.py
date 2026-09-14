from tui_creator.models import ProjectModel, ComponentModel

def generate_python_code(project: ProjectModel) -> str:
    lines = []
    
    # Header & Imports
    lines.append('"""')
    lines.append(f'Automatisch generiert mit TUI-Creator 2.0 (Valhalla Suite)')
    lines.append(f'Projekt: {project.name}')
    if project.description:
        lines.append(f'Beschreibung: {project.description}')
    lines.append('"""')
    lines.append("from textual.app import App, ComposeResult")
    lines.append("from textual.widgets import (")
    lines.append("    Button, Label, Input, Checkbox, Select, ProgressBar,")
    lines.append("    LoadingIndicator, DataTable, Rule, Header, Footer,")
    lines.append("    Switch, Markdown, OptionList, Digits, Static, Tabs")
    lines.append(")")
    lines.append("from textual.containers import Vertical, Horizontal, Container, ScrollableContainer")
    lines.append("from textual import on")
    lines.append("")
    
    safe_class_name = "".join(c for c in project.name if c.isalnum()).capitalize()
    if not safe_class_name or not safe_class_name[0].isalpha():
        safe_class_name = "MyTui"
    
    lines.append(f"class {safe_class_name}App(App):")
    lines.append(f'    """Hauptanwendung für {project.name}"""')
    lines.append(f'    TITLE = "{project.name}"')
    lines.append('    SUB_TITLE = "Erstellt mit TUI-Creator"')
    lines.append("")
    lines.append("    CSS = '''")
    lines.append("    Screen {")
    lines.append("        background: #1e1e2e;")
    lines.append("        color: #cdd6f4;")
    lines.append("    }")
    lines.append("    Header {")
    lines.append("        background: #181825;")
    lines.append("        color: #89dceb;")
    lines.append("    }")
    lines.append("    Footer {")
    lines.append("        background: #181825;")
    lines.append("        color: #a6adc8;")
    lines.append("    }")
    lines.append("    Container, Vertical, Horizontal {")
    lines.append("        padding: 1;")
    lines.append("    }")
    lines.append("    Button {")
    lines.append("        margin: 0 1;")
    lines.append("    }")
    lines.append("    Input {")
    lines.append("        background: #181825;")
    lines.append("        border: tall #45475a;")
    lines.append("        color: #cdd6f4;")
    lines.append("    }")
    lines.append("    Input:focus {")
    lines.append("        border: tall #89dceb;")
    lines.append("    }")
    lines.append("    DataTable {")
    lines.append("        background: #181825;")
    lines.append("        border: round #45475a;")
    lines.append("    }")
    lines.append("    '''")
    lines.append("")
    lines.append("    def compose(self) -> ComposeResult:")
    
    comp_counter = {"table": 0, "pb": 0}

    def walk(comp: ComponentModel, indent: int):
        ind = " " * indent
        kwargs = []
        if comp.id:
            kwargs.append(f'id="{comp.id}"')
        if comp.classes:
            kwargs.append(f'classes="{comp.classes}"')

        if comp.type == "Label":
            text = comp.props.get("text", "Text").replace('"', '\\"')
            args = [f'"{text}"'] + kwargs
            lines.append(f'{ind}yield Label({", ".join(args)})')
            
        elif comp.type == "Button":
            label = comp.props.get("label", "Button").replace('"', '\\"')
            variant = comp.props.get("variant", "primary")
            btn_kwargs = [f'variant="{variant}"'] + kwargs
            args = [f'"{label}"'] + btn_kwargs
            lines.append(f'{ind}yield Button({", ".join(args)})')
            
        elif comp.type == "Input":
            ph = comp.props.get("placeholder", "").replace('"', '\\"')
            pw = comp.props.get("password", False)
            input_kwargs = []
            if ph:
                input_kwargs.append(f'placeholder="{ph}"')
            if pw:
                input_kwargs.append('password=True')
            input_kwargs.extend(kwargs)
            lines.append(f'{ind}yield Input({", ".join(input_kwargs)})')
            
        elif comp.type == "Checkbox":
            label = comp.props.get("label", "Option").replace('"', '\\"')
            val = comp.props.get("value", False)
            cb_kwargs = []
            if val:
                cb_kwargs.append('value=True')
            cb_kwargs.extend(kwargs)
            args = [f'"{label}"'] + cb_kwargs
            lines.append(f'{ind}yield Checkbox({", ".join(args)})')

        elif comp.type == "Switch":
            val = comp.props.get("value", False)
            sw_kwargs = []
            if val:
                sw_kwargs.append('value=True')
            sw_kwargs.extend(kwargs)
            lines.append(f'{ind}yield Switch({", ".join(sw_kwargs)})')
            
        elif comp.type == "Select":
            raw_opts = comp.props.get("options", "")
            opts = [o.strip() for o in raw_opts.split(",") if o.strip()]
            if opts:
                opts_items = ", ".join([f'("{o}", "{o}")' for o in opts])
                opts_expr = f'[{opts_items}]'
            else:
                opts_expr = "[]"
            args = [opts_expr] + kwargs
            lines.append(f'{ind}yield Select({", ".join(args)})')

        elif comp.type == "OptionList":
            raw_opts = comp.props.get("options", "")
            opts = [o.strip().replace('"', '\\"') for o in raw_opts.split(",") if o.strip()]
            opts_args = [f'"{o}"' for o in opts]
            args = opts_args + kwargs
            lines.append(f'{ind}yield OptionList({", ".join(args)})')

        elif comp.type == "DataTable":
            comp_counter["table"] += 1
            tbl_var = f"tbl_{comp_counter['table']}"
            zebra = comp.props.get("zebra_stripes", True)
            dt_kwargs = [f'zebra_stripes={zebra}'] + kwargs
            lines.append(f'{ind}{tbl_var} = DataTable({", ".join(dt_kwargs)})')
            cols_str = comp.props.get("columns", "ID, Name, Status")
            cols = [c.strip().replace('"', '\\"') for c in cols_str.split(",") if c.strip()]
            for c in cols:
                lines.append(f'{ind}{tbl_var}.add_column("{c}")')
            lines.append(f'{ind}{tbl_var}.add_row("01", "Core System", "Aktiv")')
            lines.append(f'{ind}{tbl_var}.add_row("02", "Cache Layer", "Sync")')
            lines.append(f'{ind}yield {tbl_var}')

        elif comp.type == "Markdown":
            md_text = comp.props.get("markdown_text", "# Titel\\n*Markdown Inhalt*").replace('"""', "'''")
            lines.append(f'{ind}yield Markdown("""{md_text}""", {", ".join(kwargs)})')

        elif comp.type == "Digits":
            val = str(comp.props.get("value", "42:00")).replace('"', '\\"')
            lines.append(f'{ind}yield Digits("{val}", {", ".join(kwargs)})')

        elif comp.type == "Tabs":
            raw_tabs = comp.props.get("tabs", "Tab 1, Tab 2")
            tabs = [t.strip().replace('"', '\\"') for t in raw_tabs.split(",") if t.strip()]
            tabs_args = [f'"{t}"' for t in tabs] + kwargs
            lines.append(f'{ind}yield Tabs({", ".join(tabs_args)})')

        elif comp.type == "Static":
            content = comp.props.get("content", "Statischer Text").replace('"', '\\"')
            lines.append(f'{ind}yield Static("{content}", {", ".join(kwargs)})')
            
        elif comp.type == "ProgressBar":
            comp_counter["pb"] += 1
            pb_var = f"pb_{comp_counter['pb']}"
            tot = comp.props.get("total", 100)
            prog = comp.props.get("progress", 50)
            pb_kwargs = [f'total={tot}'] + kwargs
            lines.append(f'{ind}{pb_var} = ProgressBar({", ".join(pb_kwargs)})')
            lines.append(f'{ind}{pb_var}.progress = {prog}')
            lines.append(f'{ind}yield {pb_var}')
            
        elif comp.type in ("Header", "Footer", "LoadingIndicator", "Rule"):
            elem_kwargs = list(kwargs)
            if comp.type == "Header" and not comp.props.get("show_clock", True):
                elem_kwargs.insert(0, "show_clock=False")
            if comp.type == "Rule":
                ls = comp.props.get("line_style", "solid")
                elem_kwargs.insert(0, f'line_style="{ls}"')
            lines.append(f'{ind}yield {comp.type}({", ".join(elem_kwargs)})')
            
        elif comp.type in ("Container", "Vertical", "Horizontal"):
            lines.append(f'{ind}with {comp.type}({", ".join(kwargs)}):')
            if not comp.children:
                lines.append(f'{ind}    pass')
            else:
                for child in comp.children:
                    walk(child, indent + 4)

    if project.root:
        walk(project.root, 8)
    else:
        lines.append("        pass")
        
    lines.append("")
    lines.append("    # ==========================================================================")
    lines.append("    # Event Handler Boilerplate")
    lines.append("    # ==========================================================================")
    lines.append("    @on(Button.Pressed)")
    lines.append("    def handle_button_pressed(self, event: Button.Pressed) -> None:")
    lines.append('        self.notify(f"Button geklickt: {event.button.id or event.button.label}")')
    lines.append("")
    lines.append("    @on(Input.Submitted)")
    lines.append("    def handle_input_submitted(self, event: Input.Submitted) -> None:")
    lines.append('        self.notify(f"Eingabe empfangen: {event.value}")')
    lines.append("")
    lines.append("    @on(Switch.Changed)")
    lines.append("    def handle_switch_changed(self, event: Switch.Changed) -> None:")
    lines.append('        self.notify(f"Schalter [{event.switch.id}] Zustand: {event.value}")')
    lines.append("")
    lines.append("if __name__ == '__main__':")
    lines.append(f"    app = {safe_class_name}App()")
    lines.append("    app.run()")
    lines.append("")
    
    return "\n".join(lines)
