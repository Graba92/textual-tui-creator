import uuid
import time
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ComponentModel:
    type: str
    id: str = field(default_factory=lambda: f"comp_{uuid.uuid4().hex[:6]}")
    props: Dict[str, Any] = field(default_factory=dict)
    classes: str = ""
    children: List['ComponentModel'] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "id": self.id,
            "props": self.props,
            "classes": self.classes,
            "children": [c.to_dict() for c in self.children]
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'ComponentModel':
        return cls(
            type=data["type"],
            id=data.get("id", f"comp_{uuid.uuid4().hex[:6]}"),
            props=data.get("props", {}),
            classes=data.get("classes", ""),
            children=[cls.from_dict(c) for c in data.get("children", [])]
        )

    def clone(self) -> 'ComponentModel':
        new_id = f"{self.type.lower()}_{uuid.uuid4().hex[:6]}"
        cloned_children = [c.clone() for c in self.children]
        return ComponentModel(
            type=self.type,
            id=new_id,
            props=dict(self.props),
            classes=self.classes,
            children=cloned_children
        )

@dataclass
class ProjectModel:
    name: str
    description: str = ""
    id: str = field(default_factory=lambda: f"proj_{uuid.uuid4().hex[:8]}")
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    root: Optional[ComponentModel] = None

    def __post_init__(self):
        if self.root is None:
            self.root = ComponentModel(type="Vertical", id="root_container")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "root": self.root.to_dict() if self.root else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'ProjectModel':
        project = cls(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            created_at=data.get("created_at", time.time()),
            updated_at=data.get("updated_at", time.time())
        )
        if data.get("root"):
            project.root = ComponentModel.from_dict(data["root"])
        return project
