#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit-Tests für Textual TUI-Creator
Testet i18n Lokalisierung, Model-Serialisierung, Template-Erstellung und Code-Generator.
"""

import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from tui_creator.i18n import t, set_language, get_language, toggle_language
from tui_creator.models import ProjectModel, ComponentModel
from tui_creator.storage import get_available_templates, create_template_project
from tui_creator.generator import generate_python_code


class TestTuiCreator(unittest.TestCase):

    def setUp(self):
        set_language("de")

    def tearDown(self):
        set_language("de")

    def test_i18n_translation(self):
        set_language("de")
        self.assertEqual(get_language(), "de")
        self.assertIn("Neues Projekt", t("btn_new_project"))
        self.assertEqual(t("btn_cancel"), "Abbrechen")

        set_language("en")
        self.assertEqual(get_language(), "en")
        self.assertIn("New Project", t("btn_new_project"))
        self.assertEqual(t("btn_cancel"), "Cancel")

    def test_i18n_toggle(self):
        set_language("de")
        self.assertEqual(toggle_language(), "en")
        self.assertEqual(toggle_language(), "de")

    def test_models_serialization(self):
        comp = ComponentModel(type="Button", id="btn_test", props={"label": "Click Me"})
        root = ComponentModel(type="Vertical", id="root", children=[comp])
        proj = ProjectModel(id="test_id", name="Test Project", root=root)

        data = proj.to_dict()
        self.assertEqual(data["name"], "Test Project")
        self.assertEqual(len(data["root"]["children"]), 1)

        restored = ProjectModel.from_dict(data)
        self.assertEqual(restored.name, "Test Project")
        self.assertEqual(restored.root.children[0].type, "Button")

    def test_templates_creation(self):
        templates = get_available_templates()
        self.assertIn("blank", templates)
        self.assertIn("dashboard", templates)

        proj = create_template_project("dashboard", "DashboardApp")
        self.assertEqual(proj.name, "DashboardApp")
        self.assertIsNotNone(proj.root)

    def test_code_generation(self):
        proj = create_template_project("blank", "BlankApp")
        code = generate_python_code(proj)
        self.assertIn("class BlankappApp(App):", code)
        self.assertIn("def compose(self) -> ComposeResult:", code)


if __name__ == "__main__":
    unittest.main()
