import json
import os
import time
from pathlib import Path
from typing import List, Optional
from tui_creator.models import ProjectModel, ComponentModel

def get_data_dir() -> Path:
    base_dir = Path.home() / ".local" / "share" / "tui-creator"
    projects_dir = base_dir / "projects"
    exports_dir = base_dir / "exports"
    
    projects_dir.mkdir(parents=True, exist_ok=True)
    exports_dir.mkdir(parents=True, exist_ok=True)
    
    return base_dir

def get_projects_dir() -> Path:
    return get_data_dir() / "projects"

def get_exports_dir() -> Path:
    return get_data_dir() / "exports"

def get_available_templates() -> dict:
    return {
        "blank": {"name": "Leeres Projekt", "desc": "Standard-Container ohne vordefinierte Widgets"},
        "dashboard": {"name": "System-Dashboard", "desc": "Header, Status-Karten, Digits, DataTable und Footer"},
        "form": {"name": "Eingabeformular", "desc": "Text-Felder, Dropdown, Checkboxen, Schalter und Aktions-Buttons"},
        "master_detail": {"name": "Master-Detail Ansicht", "desc": "Linke Optionsliste als Navigation, rechter Inhaltsbereich mit Markdown"}
    }

def create_template_project(template_key: str, project_name: str) -> ProjectModel:
    project = ProjectModel(name=project_name)
    if template_key == "dashboard":
        project.root = ComponentModel(
            type="Vertical", id="root_container",
            children=[
                ComponentModel(type="Header", id="main_header", props={"show_clock": True}),
                ComponentModel(
                    type="Horizontal", id="stats_panel",
                    children=[
                        ComponentModel(type="Container", id="card_cpu", children=[
                            ComponentModel(type="Label", id="lbl_cpu", props={"text": "CPU Auslastung"}),
                            ComponentModel(type="Digits", id="dig_cpu", props={"value": "18%"}),
                        ]),
                        ComponentModel(type="Container", id="card_ram", children=[
                            ComponentModel(type="Label", id="lbl_ram", props={"text": "RAM Verbrauch"}),
                            ComponentModel(type="Digits", id="dig_ram", props={"value": "3.8G"}),
                        ]),
                        ComponentModel(type="Container", id="card_tasks", children=[
                            ComponentModel(type="Label", id="lbl_tasks", props={"text": "Aktive Tasks"}),
                            ComponentModel(type="Digits", id="dig_tasks", props={"value": "94"}),
                        ]),
                    ]
                ),
                ComponentModel(type="DataTable", id="metrics_table", props={"columns": "PID, Service, Status, CPU, RAM", "zebra_stripes": True}),
                ComponentModel(type="ProgressBar", id="load_bar", props={"total": 100, "progress": 45}),
                ComponentModel(type="Footer", id="main_footer")
            ]
        )
    elif template_key == "form":
        project.root = ComponentModel(
            type="Vertical", id="root_container",
            children=[
                ComponentModel(type="Header", id="main_header", props={"show_clock": True}),
                ComponentModel(type="Label", id="form_title", props={"text": "Benutzerprofil & Systemeinstellungen"}),
                ComponentModel(type="Input", id="txt_user", props={"placeholder": "Benutzername eingeben..."}),
                ComponentModel(type="Input", id="txt_mail", props={"placeholder": "E-Mail-Adresse..."}),
                ComponentModel(type="Input", id="txt_pwd", props={"placeholder": "Sicheres Passwort...", "password": True}),
                ComponentModel(type="Select", id="sel_role", props={"options": "Admin, Entwickler, Operator, Gast"}),
                ComponentModel(type="Switch", id="sw_active", props={"value": True}),
                ComponentModel(type="Checkbox", id="chk_notify", props={"label": "Echtzeit-Benachrichtigungen aktivieren", "value": True}),
                ComponentModel(
                    type="Horizontal", id="btn_row",
                    children=[
                        ComponentModel(type="Button", id="btn_reset", props={"label": "Zurücksetzen", "variant": "error"}),
                        ComponentModel(type="Button", id="btn_save", props={"label": "Speichern & Anwenden", "variant": "success"}),
                    ]
                ),
                ComponentModel(type="Footer", id="main_footer")
            ]
        )
    elif template_key == "master_detail":
        project.root = ComponentModel(
            type="Vertical", id="root_container",
            children=[
                ComponentModel(type="Header", id="main_header", props={"show_clock": True}),
                ComponentModel(
                    type="Horizontal", id="master_layout",
                    children=[
                        ComponentModel(type="Vertical", id="sidebar", children=[
                            ComponentModel(type="Label", id="lbl_nav", props={"text": "📁 Navigation"}),
                            ComponentModel(type="OptionList", id="nav_list", props={"options": "Übersicht, Prozesse, Netzwerkanalyse, Hardware-Status, Logs"}),
                        ]),
                        ComponentModel(type="Vertical", id="content_area", children=[
                            ComponentModel(type="Markdown", id="md_doc", props={"markdown_text": "# Valhalla System Monitor\\n\\n*Wähle links einen Menüpunkt aus, um Live-Metriken zu laden.*\\n\\n- Integriert mit **CachyOS**\\n- Wayland & KWin optimiert"}),
                            ComponentModel(type="ProgressBar", id="sync_progress", props={"total": 100, "progress": 80}),
                            ComponentModel(type="Button", id="btn_refresh", props={"label": "Daten aktualisieren", "variant": "primary"}),
                        ])
                    ]
                ),
                ComponentModel(type="Footer", id="main_footer")
            ]
        )
    else:
        project.root = ComponentModel(type="Vertical", id="root_container")
    return project

def list_projects() -> List[dict]:
    projects = []
    p_dir = get_projects_dir()
    for file_path in p_dir.glob("*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                projects.append({
                    "id": data.get("id", file_path.stem),
                    "name": data.get("name", "Unbenannt"),
                    "updated_at": data.get("updated_at", 0),
                    "file_path": str(file_path)
                })
        except Exception:
            pass
    
    projects.sort(key=lambda x: x["updated_at"], reverse=True)
    return projects

def load_project(project_id: str) -> Optional[ProjectModel]:
    p_dir = get_projects_dir()
    direct_file = p_dir / f"{project_id}.json"
    if direct_file.exists():
        try:
            with open(direct_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return ProjectModel.from_dict(data)
        except Exception as e:
            raise ValueError(f"Projektdatei ist beschädigt: {e}")
            
    for file_path in p_dir.glob("*.json"):
        if file_path.stem == project_id or project_id in str(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return ProjectModel.from_dict(data)
            except Exception as e:
                raise ValueError(f"Projektdatei ist beschädigt: {e}")
    return None

def save_project(project: ProjectModel) -> None:
    project.updated_at = time.time()
    file_path = get_projects_dir() / f"{project.id}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(project.to_dict(), f, indent=4, ensure_ascii=False)

def delete_project(project_id: str) -> bool:
    p_dir = get_projects_dir()
    file_path = p_dir / f"{project_id}.json"
    if file_path.exists():
        try:
            os.remove(file_path)
            return True
        except Exception:
            return False
    return False

def export_python_code(project_name: str, code: str) -> Path:
    safe_name = "".join(c for c in project_name if c.isalnum() or c in " _-").strip().replace(" ", "_").lower()
    if not safe_name:
        safe_name = "exported_tui"
    file_path = get_exports_dir() / f"{safe_name}.py"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)
    return file_path
