import json
import time
from typing import Optional, Dict, Any, List
from rich.syntax import Syntax

from textual.app import ComposeResult
from textual.screen import Screen, ModalScreen
from textual.widgets import (
    Header, Footer, Button, Label, Input, Tree, Switch, Select,
    ListItem, ListView, Tabs, Tab, Static
)
from textual.containers import Vertical, Horizontal, VerticalScroll, Container, ScrollableContainer
from textual.binding import Binding
from textual import on

from tui_creator.models import ProjectModel, ComponentModel
from tui_creator.storage import (
    list_projects, load_project, save_project, delete_project,
    export_python_code, get_available_templates, create_template_project
)
from tui_creator.components import COMPONENT_REGISTRY, COMPONENT_ICONS, create_preview_widget
from tui_creator.generator import generate_python_code
from tui_creator.i18n import t, set_language, get_language, toggle_language


class ConfirmDialog(ModalScreen[bool]):
    """Bestätigungsdialog für kritische Aktionen."""
    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Label(self.message, id="dialog-msg")
            with Horizontal(id="dialog-buttons"):
                yield Button(t("btn_cancel"), variant="default", id="btn-cancel")
                yield Button(t("btn_confirm"), variant="error", id="btn-ok")

    @on(Button.Pressed, "#btn-cancel")
    def cancel(self):
        self.dismiss(False)

    @on(Button.Pressed, "#btn-ok")
    def confirm(self):
        self.dismiss(True)


class InputDialog(ModalScreen[Optional[str]]):
    """Generischer Dialog zur Texteingabe."""
    def __init__(self, title: str, default: str = ""):
        super().__init__()
        self.title = title
        self.default = default

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Label(self.title, classes="prop-header")
            yield Input(value=self.default, id="dialog-input")
            with Horizontal(id="dialog-buttons"):
                yield Button(t("btn_cancel"), variant="error", id="btn-cancel")
                yield Button(t("btn_save"), variant="success", id="btn-ok")

    def on_mount(self):
        self.query_one(Input).focus()

    @on(Button.Pressed, "#btn-cancel")
    def cancel(self):
        self.dismiss(None)

    @on(Button.Pressed, "#btn-ok")
    def confirm(self):
        self.dismiss(self.query_one(Input).value)


class NewProjectDialog(ModalScreen[Optional[dict]]):
    """Dialog zur Erstellung eines neuen Projekts (Blank oder aus Vorlage)."""
    def compose(self) -> ComposeResult:
        templates = get_available_templates()
        tpl_options = [(info["name"], key) for key, info in templates.items()]

        with Vertical(id="dialog", classes="large-dialog"):
            yield Label(t("new_proj_dialog_title"), classes="prop-header")
            yield Label(t("lbl_proj_name"), classes="prop-label")
            yield Input(placeholder="MeinTuiProjekt", id="input-proj-name")
            
            yield Label(t("lbl_choose_template"), classes="prop-label")
            yield Select(options=tpl_options, value="blank", id="select-template", allow_blank=False)
            
            yield Label("", id="lbl-template-desc", classes="subtitle")
            
            with Horizontal(id="dialog-buttons"):
                yield Button(t("btn_cancel"), variant="error", id="btn-cancel")
                yield Button(t("btn_create_proj"), variant="success", id="btn-create-proj")

    def on_mount(self):
        self.update_desc("blank")
        self.query_one("#input-proj-name", Input).focus()

    @on(Select.Changed, "#select-template")
    def on_tpl_changed(self, event: Select.Changed):
        self.update_desc(str(event.value))

    def update_desc(self, tpl_key: str):
        templates = get_available_templates()
        desc = templates.get(tpl_key, {}).get("desc", "")
        self.query_one("#lbl-template-desc", Label).update(f"ℹ {desc}")

    @on(Button.Pressed, "#btn-cancel")
    def cancel(self):
        self.dismiss(None)

    @on(Button.Pressed, "#btn-create-proj")
    def create_project(self):
        name = self.query_one("#input-proj-name", Input).value.strip()
        tpl = str(self.query_one("#select-template", Select).value)
        if not name:
            name = "Unbenanntes_Projekt"
        self.dismiss({"name": name, "template": tpl})


class ComponentSelectDialog(ModalScreen[Optional[str]]):
    """Dialog zur Auswahl einer Komponente aus der erweiterten Bibliothek."""
    def compose(self) -> ComposeResult:
        with Vertical(id="dialog", classes="large-dialog"):
            yield Label("Komponente zur Einfügung wählen:", classes="prop-header")
            with ListView(id="comp-list"):
                for comp_type, info in COMPONENT_REGISTRY.items():
                    icon = COMPONENT_ICONS.get(comp_type, "🔹")
                    is_cont = " [Container]" if info.get("container") else ""
                    text = f"{icon} [bold]{comp_type}[/bold]{is_cont}  ─  [dim]{info['desc']}[/dim]"
                    yield ListItem(Label(text), id=comp_type)
            with Horizontal(id="dialog-buttons"):
                yield Button("Abbrechen", variant="error", id="btn-cancel")

    @on(ListView.Selected)
    def selected(self, event: ListView.Selected):
        self.dismiss(str(event.item.id) if event.item.id else None)

    @on(Button.Pressed, "#btn-cancel")
    def cancel(self):
        self.dismiss(None)


class StartScreen(Screen):
    """Start- und Projektverwaltungs-Bildschirm."""
    BINDINGS = [
        Binding("escape", "quit", "Beenden / Quit"),
        Binding("q", "quit", "Beenden / Quit"),
        Binding("n", "new_project", "Neues Projekt / New Project"),
        Binding("t", "new_from_template", "Aus Vorlage / Template"),
        Binding("d", "delete_selected", "Löschen / Delete"),
        Binding("l", "toggle_lang", "🌐 DE/EN"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(id="start-container"):
            yield Label(f"⚡ {t('start_title')}", id="main-title")
            yield Label(t("start_subtitle"), classes="subtitle")
            
            with Horizontal(id="start-actions"):
                yield Button(f"{t('btn_new_project')} [n]", variant="success", id="btn-new")
                yield Button(f"{t('btn_delete_project')} [d]", variant="error", id="btn-delete-proj")
                yield Button(t("btn_lang_toggle"), variant="warning", id="btn-lang")
            
            yield Label(t("start_projects_title"), id="lbl-projects-header", classes="section-title")
            yield ListView(id="project-list")
            
        yield Footer()

    def action_toggle_lang(self):
        new_lang = toggle_language()
        self.notify(f"Sprache gewechselt zu: {new_lang.upper()}", timeout=2.0)
        self.query_one("#btn-lang", Button).label = t("btn_lang_toggle")
        self.query_one("#btn-new", Button).label = f"{t('btn_new_project')} [n]"
        self.query_one("#btn-delete-proj", Button).label = f"{t('btn_delete_project')} [d]"
        self.query_one("#lbl-projects-header", Label).update(t("start_projects_title"))
        self.refresh_projects()

    def on_mount(self):
        self.refresh_projects()

    def refresh_projects(self):
        list_view = self.query_one("#project-list", ListView)
        list_view.clear()
        projects = list_projects()
        if not projects:
            list_view.append(ListItem(Label("[dim]Keine Projekte vorhanden. Klicke auf 'Neues Projekt'.[/dim]"), id="dummy_none"))
            return

        for p in projects:
            formatted_time = time.strftime("%d.%m.%Y %H:%M", time.localtime(p["updated_at"])) if p["updated_at"] else "Neu"
            item_text = f"📁 [bold cyan]{p['name']}[/bold cyan]  [dim]│ ID: {p['id']} │ Zuletzt: {formatted_time}[/dim]"
            list_view.append(ListItem(Label(item_text), id=p['id']))

    def action_new_project(self):
        self.new_project()

    def action_new_from_template(self):
        self.new_project()

    @on(Button.Pressed, "#btn-new")
    def new_project(self):
        def on_dialog_result(result: Optional[dict]):
            if result:
                name = result["name"]
                template = result["template"]
                project = create_template_project(template, name)
                save_project(project)
                self.app.switch_to_editor(project)

        self.app.push_screen(NewProjectDialog(), on_dialog_result)

    @on(ListView.Selected, "#project-list")
    def open_project(self, event: ListView.Selected):
        if not event.item or not event.item.id or event.item.id == "dummy_none":
            return
        try:
            project = load_project(str(event.item.id))
            if project:
                self.app.switch_to_editor(project)
            else:
                self.app.notify("Projekt konnte nicht geladen werden.", severity="error")
        except Exception as e:
            self.app.notify(str(e), severity="error")

    def action_delete_selected(self):
        self.delete_selected_project()

    @on(Button.Pressed, "#btn-delete-proj")
    def delete_selected_project(self):
        list_view = self.query_one("#project-list", ListView)
        if list_view.highlighted_child and list_view.highlighted_child.id and list_view.highlighted_child.id != "dummy_none":
            proj_id = str(list_view.highlighted_child.id)
            def on_confirm(confirm: bool):
                if confirm:
                    if delete_project(proj_id):
                        self.refresh_projects()
                        self.app.notify("Projekt erfolgreich gelöscht.")
                    else:
                        self.app.notify("Fehler beim Löschen des Projekts.", severity="error")
            self.app.push_screen(ConfirmDialog("Möchtest du das ausgewählte Projekt wirklich löschen?"), on_confirm)
        else:
            self.app.notify("Kein gültiges Projekt ausgewählt.", severity="warning")


class EditorScreen(Screen):
    """
    Hauptarbeitsbereich:
    3-Spalten Layout:
    - Links: Strukturbaum mit Icons und Sortier-Werkzeugen (Up, Down, Clone, Del)
    - Mitte: Tabbed View (👁️ Live-Vorschau vs. 💻 Python-Code)
    - Rechts: Eigenschafts-Inspektor mit typisierten Eingabefeldern
    """
    BINDINGS = [
        Binding("ctrl+s", "save", "Speichern / Save"),
        Binding("ctrl+z", "undo", "Rückgängig / Undo"),
        Binding("ctrl+y", "redo", "Wiederholen / Redo"),
        Binding("ctrl+e", "export_code", "Exportieren / Export"),
        Binding("f1", "help", "Hilfe / Help"),
        Binding("f5", "refresh_view", "Aktualisieren / Refresh"),
        Binding("l", "toggle_lang", "🌐 DE/EN"),
        Binding("escape", "back", "Zurück / Back"),
    ]

    def __init__(self, project: ProjectModel):
        super().__init__()
        self.project = project
        self.undo_stack: List[str] = []
        self.redo_stack: List[str] = []
        self.selected_node_id: Optional[str] = None
        self.active_center_tab: str = "preview"
        
        if not self.project.root:
            self.project.root = ComponentModel(type="Vertical", id="root_container")
        self.selected_node_id = self.project.root.id

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="editor-layout"):
            # Linke Spalte: Struktur & Hierarchie
            with Vertical(id="left-panel"):
                yield Label(f"📁 {t('editor_panel_components')}", id="lbl-left-panel", classes="panel-title")
                yield Tree("Projekt", id="comp-tree")
                with Horizontal(id="tree-actions"):
                    yield Button("+", id="btn-add", tooltip=t("btn_add_component"), variant="success")
                    yield Button("▲", id="btn-move-up", tooltip="Nach oben", variant="default")
                    yield Button("▼", id="btn-move-down", tooltip="Nach unten", variant="default")
                    yield Button("📋", id="btn-clone", tooltip="Duplizieren", variant="primary")
                    yield Button("✖", id="btn-del", tooltip=t("btn_remove_component"), variant="error")
                    
            # Mittlere Spalte: Live-Vorschau & Python-Code
            with Vertical(id="center-panel"):
                yield Tabs("👁️ Live-Vorschau", "💻 Generierter Python-Code", id="center-tabs")
                
                with Container(id="preview-container"):
                    pass

                with ScrollableContainer(id="code-view-container"):
                    yield Static("", id="code-view-text")
                
                with Horizontal(id="preview-actions"):
                    yield Button(f"💾 {t('btn_save')} [Ctrl+S]", variant="success", id="btn-save")
                    yield Button(f"🚀 {t('btn_export_code')} [Ctrl+E]", variant="primary", id="btn-export")
                    yield Button("⚡ Aktualisieren [F5]", variant="default", id="btn-refresh")
                    
            # Rechte Spalte: Eigenschaften-Inspektor
            with Vertical(id="right-panel"):
                yield Label(f"⚙️ {t('editor_panel_props')}", id="lbl-right-panel", classes="panel-title")
                with VerticalScroll(id="props-container"):
                    yield Label(t("lbl_no_selection"), id="lbl-props-empty")
                yield Button("✔ Änderungen anwenden", variant="success", id="btn-apply-props")

        yield Footer()

    def action_toggle_lang(self):
        new_lang = toggle_language()
        self.notify(f"Sprache gewechselt zu: {new_lang.upper()}", timeout=2.0)
        self.query_one("#lbl-left-panel", Label).update(f"📁 {t('editor_panel_components')}")
        self.query_one("#lbl-right-panel", Label).update(f"⚙️ {t('editor_panel_props')}")
        self.query_one("#btn-save", Button).label = f"💾 {t('btn_save')} [Ctrl+S]"
        self.query_one("#btn-export", Button).label = f"🚀 {t('btn_export_code')} [Ctrl+E]"

    async def on_mount(self):
        # Initial: Preview sichtbar, Code ausgeblendet
        self.query_one("#code-view-container").display = False
        await self.refresh_all()

    def save_state(self):
        self.undo_stack.append(json.dumps(self.project.to_dict()))
        self.redo_stack.clear()

    async def action_undo(self):
        if self.undo_stack:
            self.redo_stack.append(json.dumps(self.project.to_dict()))
            state = self.undo_stack.pop()
            self.project = ProjectModel.from_dict(json.loads(state))
            await self.refresh_all()
            self.app.notify("Rückgängig gemacht.")

    async def action_redo(self):
        if self.redo_stack:
            self.undo_stack.append(json.dumps(self.project.to_dict()))
            state = self.redo_stack.pop()
            self.project = ProjectModel.from_dict(json.loads(state))
            await self.refresh_all()
            self.app.notify("Wiederholt.")

    def action_save(self):
        try:
            save_project(self.project)
            self.app.notify("Projekt erfolgreich gespeichert.", severity="information")
        except Exception as e:
            self.app.notify(f"Fehler beim Speichern: {e}", severity="error")

    @on(Button.Pressed, "#btn-save")
    def on_save_btn(self):
        self.action_save()

    def action_back(self):
        def check_save(confirm: bool):
            if confirm:
                self.action_save()
            self.app.switch_to_start()
            
        self.app.push_screen(ConfirmDialog("Ungespeicherte Änderungen vor dem Beenden speichern?"), check_save)

    def action_help(self):
        msg = (
            "Bedienung:\n"
            "• Linke Spalte: Strukturbaum aufbauen (+ für neue Komponenten, ▲/▼ zum Verschieben, 📋 zum Klonen).\n"
            "• Mittlere Spalte: Live-Vorschau und generierter Python-Code per Tab umschaltbar.\n"
            "• Rechte Spalte: Eigenschaften gezielt editieren & mit 'Änderungen anwenden' übernehmen.\n\n"
            "Tastenkürzel:\n"
            "• Strg+S: Speichern  │  Strg+E: Code exportieren\n"
            "• Strg+Z: Rückgängig  │  Strg+Y: Wiederholen\n"
            "• F5: Ansicht aktualisieren  │  Esc: Zurück"
        )
        self.app.notify(msg, title="TUI-Creator Hilfe", timeout=10)

    async def action_refresh_view(self):
        await self.refresh_all()
        self.app.notify("Ansicht aktualisiert.")

    @on(Button.Pressed, "#btn-refresh")
    async def on_refresh_btn(self):
        await self.action_refresh_view()

    @on(Tabs.TabActivated, "#center-tabs")
    async def on_tab_activated(self, event: Tabs.TabActivated):
        prev_container = self.query_one("#preview-container")
        code_container = self.query_one("#code-view-container")
        
        if "Python-Code" in str(event.tab.label):
            self.active_center_tab = "code"
            prev_container.display = False
            code_container.display = True
            await self.update_code_view()
        else:
            self.active_center_tab = "preview"
            code_container.display = False
            prev_container.display = True
            await self.update_preview()

    async def refresh_all(self):
        self.update_tree()
        if self.active_center_tab == "preview":
            await self.update_preview()
        else:
            await self.update_code_view()
        await self.update_props_panel()

    def _find_component(self, node: Optional[ComponentModel], target_id: str) -> Optional[ComponentModel]:
        if not node:
            return None
        if node.id == target_id:
            return node
        for child in node.children:
            res = self._find_component(child, target_id)
            if res:
                return res
        return None

    def _find_parent(self, node: Optional[ComponentModel], target_id: str) -> Optional[ComponentModel]:
        if not node:
            return None
        for child in node.children:
            if child.id == target_id:
                return node
            res = self._find_parent(child, target_id)
            if res:
                return res
        return None

    def update_tree(self):
        tree = self.query_one("#comp-tree", Tree)
        tree.clear()
        
        def build_node(comp: ComponentModel, tree_node):
            icon = COMPONENT_ICONS.get(comp.type, "🔹")
            label = f"{icon} {comp.type} [dim](#{comp.id})[/dim]"
            new_node = tree_node.add(label, data=comp.id)
            for child in comp.children:
                build_node(child, new_node)
                
        tree.root.data = "root_dummy"
        if self.project.root:
            build_node(self.project.root, tree.root)
        tree.root.expand_all()

    async def update_preview(self):
        container = self.query_one("#preview-container", Container)
        await container.remove_children()

        def build_ui(comp: ComponentModel):
            w = create_preview_widget(comp.type, comp.id, comp.props, comp.classes)
            if COMPONENT_REGISTRY.get(comp.type, {}).get("container", False):
                for child in comp.children:
                    child_w = build_ui(child)
                    if child_w:
                        w.compose_add_child(child_w)
            return w

        try:
            if self.project.root:
                root_widget = build_ui(self.project.root)
                if root_widget:
                    await container.mount(root_widget)
        except Exception as e:
            await container.mount(Label(f"Fehler beim Rendern der Vorschau: {e}", classes="error-label"))

    async def update_code_view(self):
        try:
            code = generate_python_code(self.project)
            code_text = self.query_one("#code-view-text", Static)
            syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
            code_text.update(syntax)
        except Exception as e:
            self.app.notify(f"Fehler bei Codegenerierung: {e}", severity="error")

    @on(Tree.NodeSelected)
    async def on_tree_selected(self, event: Tree.NodeSelected):
        if event.node.data and event.node.data != "root_dummy":
            self.selected_node_id = str(event.node.data)
            await self.update_props_panel()

    @on(Tree.NodeHighlighted)
    async def on_tree_highlighted(self, event: Tree.NodeHighlighted):
        if event.node.data and event.node.data != "root_dummy":
            self.selected_node_id = str(event.node.data)
            await self.update_props_panel()

    async def update_props_panel(self):
        container = self.query_one("#props-container", VerticalScroll)
        await container.remove_children()
        
        if not self.selected_node_id:
            await container.mount(Label("Keine Komponente ausgewählt."))
            return
            
        comp = self._find_component(self.project.root, self.selected_node_id)
        if not comp:
            await container.mount(Label("Komponente nicht gefunden."))
            return
        
        icon = COMPONENT_ICONS.get(comp.type, "🔹")
        await container.mount(Label(f"{icon} Komponente: {comp.type}", classes="prop-header"))
        await container.mount(Label("Widget-ID:", classes="prop-label"))
        await container.mount(Input(value=comp.id, id="prop-id"))
        await container.mount(Label("CSS-Klassen:", classes="prop-label"))
        await container.mount(Input(value=comp.classes, id="prop-classes"))
        
        for p_name, p_val in comp.props.items():
            await container.mount(Label(f"{p_name.capitalize()}:", classes="prop-label"))
            if isinstance(p_val, bool):
                await container.mount(Switch(value=p_val, id=f"prop-val-{p_name}"))
            elif p_name == "variant":
                variants = [("Primary", "primary"), ("Secondary", "secondary"), ("Success", "success"), ("Warning", "warning"), ("Error", "error"), ("Default", "default")]
                await container.mount(Select(options=variants, value=str(p_val), id=f"prop-val-{p_name}", allow_blank=False))
            elif p_name == "line_style":
                styles = [("Solid", "solid"), ("Double", "double"), ("Heavy", "heavy"), ("Dashed", "dashed")]
                await container.mount(Select(options=styles, value=str(p_val), id=f"prop-val-{p_name}", allow_blank=False))
            else:
                await container.mount(Input(value=str(p_val), id=f"prop-val-{p_name}"))

    @on(Button.Pressed, "#btn-apply-props")
    async def apply_props(self):
        if not self.selected_node_id:
            return
        comp = self._find_component(self.project.root, self.selected_node_id)
        if not comp:
            return
        
        self.save_state()
        
        id_input = self.query_one("#prop-id", Input).value.strip()
        if id_input:
            comp.id = id_input
            self.selected_node_id = comp.id
            
        comp.classes = self.query_one("#prop-classes", Input).value.strip()
        
        for p_name in list(comp.props.keys()):
            try:
                widget = self.query_one(f"#prop-val-{p_name}")
                if isinstance(widget, Switch):
                    comp.props[p_name] = widget.value
                elif isinstance(widget, Select):
                    comp.props[p_name] = str(widget.value)
                elif isinstance(widget, Input):
                    orig = COMPONENT_REGISTRY.get(comp.type, {}).get("props", {}).get(p_name, "")
                    if isinstance(orig, int):
                        try:
                            comp.props[p_name] = int(widget.value)
                        except ValueError:
                            pass
                    elif isinstance(orig, float):
                        try:
                            comp.props[p_name] = float(widget.value)
                        except ValueError:
                            pass
                    else:
                        comp.props[p_name] = widget.value
            except Exception:
                pass
                        
        await self.refresh_all()
        self.app.notify("Eigenschaften erfolgreich angewendet.", severity="information")

    @on(Button.Pressed, "#btn-add")
    def add_component(self):
        def on_selected(comp_type: Optional[str]):
            if comp_type:
                self.save_state()
                default_props = COMPONENT_REGISTRY[comp_type]["props"].copy()
                new_comp = ComponentModel(type=comp_type, props=default_props)
                
                target = self._find_component(self.project.root, self.selected_node_id) if self.selected_node_id else self.project.root
                if not target:
                    target = self.project.root
                
                if target and COMPONENT_REGISTRY.get(target.type, {}).get("container", False):
                    target.children.append(new_comp)
                else:
                    parent = self._find_parent(self.project.root, target.id) if target else None
                    if parent:
                        parent.children.append(new_comp)
                    elif self.project.root:
                        self.project.root.children.append(new_comp)
                        
                self.selected_node_id = new_comp.id
                self.run_worker(self.refresh_all())
                
        self.app.push_screen(ComponentSelectDialog(), on_selected)

    @on(Button.Pressed, "#btn-del")
    def delete_component(self):
        if not self.selected_node_id or (self.project.root and self.selected_node_id == self.project.root.id):
            self.app.notify("Das Stamm-Element kann nicht gelöscht werden.", severity="warning")
            return
            
        def on_confirm(confirm: bool):
            if confirm:
                self.save_state()
                parent = self._find_parent(self.project.root, self.selected_node_id)
                if parent:
                    parent.children = [c for c in parent.children if c.id != self.selected_node_id]
                    self.selected_node_id = parent.id
                    self.run_worker(self.refresh_all())
                    
        self.app.push_screen(ConfirmDialog("Komponente wirklich löschen?"), on_confirm)

    @on(Button.Pressed, "#btn-clone")
    def clone_component(self):
        if not self.selected_node_id or (self.project.root and self.selected_node_id == self.project.root.id):
            self.app.notify("Stamm-Element kann nicht dupliziert werden.", severity="warning")
            return

        parent = self._find_parent(self.project.root, self.selected_node_id)
        if not parent:
            self.app.notify("Kein Eltern-Element gefunden.", severity="warning")
            return

        comp = self._find_component(self.project.root, self.selected_node_id)
        if not comp:
            return

        self.save_state()
        cloned = comp.clone()
        parent.children.append(cloned)
        self.selected_node_id = cloned.id
        self.run_worker(self.refresh_all())
        self.app.notify(f"Komponente dupliziert ({cloned.id}).", severity="information")

    @on(Button.Pressed, "#btn-move-up")
    def move_up(self):
        self._move_component_delta(-1)

    @on(Button.Pressed, "#btn-move-down")
    def move_down(self):
        self._move_component_delta(1)

    def _move_component_delta(self, delta: int):
        if not self.selected_node_id or (self.project.root and self.selected_node_id == self.project.root.id):
            return

        parent = self._find_parent(self.project.root, self.selected_node_id)
        if not parent or not parent.children:
            return

        idx = -1
        for i, c in enumerate(parent.children):
            if c.id == self.selected_node_id:
                idx = i
                break

        if idx == -1:
            return

        new_idx = idx + delta
        if 0 <= new_idx < len(parent.children):
            self.save_state()
            parent.children[idx], parent.children[new_idx] = parent.children[new_idx], parent.children[idx]
            self.run_worker(self.refresh_all())
            self.app.notify("Reihenfolge geändert.")

    def action_export_code(self):
        self.export_code()

    @on(Button.Pressed, "#btn-export")
    def export_code(self):
        try:
            code = generate_python_code(self.project)
            path = export_python_code(self.project.name, code)
            self.app.notify(f"Python-Code erfolgreich exportiert nach:\n{path}", title="Export Erfolgreich", timeout=8)
        except Exception as e:
            self.app.notify(f"Export fehlgeschlagen: {e}", severity="error")
