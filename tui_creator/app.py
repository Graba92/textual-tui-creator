from textual.app import App
from tui_creator.ui import StartScreen, EditorScreen
from tui_creator.models import ProjectModel

class TuiCreatorApp(App):
    TITLE = "TUI-Creator"
    
    CSS = """
    Screen {
        background: #11111b;
        color: #cdd6f4;
    }
    
    Header {
        background: #181825;
        color: #89dceb;
    }
    
    Footer {
        background: #181825;
        color: #a6adc8;
    }
    
    #main-title {
        text-align: center;
        content-align: center middle;
        text-style: bold;
        color: #89dceb;
        height: 3;
    }
    
    .subtitle {
        text-align: center;
        color: #a6adc8;
        margin-bottom: 2;
    }
    
    .section-title {
        text-style: bold;
        margin-top: 1;
        margin-bottom: 1;
        color: #f9e2af;
    }
    
    #start-container {
        align: center top;
        padding: 2 4;
        width: 100%;
        height: 100%;
        background: #1e1e2e;
    }
    
    #start-actions {
        height: auto;
        align: center middle;
        margin-bottom: 2;
    }
    
    #start-actions Button {
        margin: 0 1;
    }
    
    #project-list {
        height: 1fr;
        border: solid #45475a;
        background: #181825;
    }
    #project-list:focus {
        border: solid #89dceb;
    }
    
    #editor-layout {
        height: 100%;
    }
    
    .panel-title {
        background: #181825;
        color: #89dceb;
        text-align: center;
        text-style: bold;
        width: 100%;
        padding: 1;
        border-bottom: solid #313244;
    }
    
    #left-panel {
        width: 36;
        border-right: solid #313244;
        height: 100%;
        background: #181825;
    }
    
    #comp-tree {
        background: #181825;
        color: #cdd6f4;
        height: 1fr;
    }
    
    #center-panel {
        width: 1fr;
        height: 100%;
        background: #1e1e2e;
    }
    
    #right-panel {
        width: 38;
        border-left: solid #313244;
        height: 100%;
        padding: 0 1;
        background: #181825;
    }
    
    #props-container {
        height: 1fr;
        padding: 1;
    }
    
    #preview-container {
        height: 1fr;
        border: round #45475a;
        margin: 1;
        padding: 1;
        background: #11111b;
    }
    
    #code-view-container {
        height: 1fr;
        border: round #45475a;
        margin: 1;
        padding: 1;
        background: #11111b;
        color: #a6e3a1;
    }
    
    #tree-actions {
        height: 3;
        align: center middle;
        background: #181825;
        border-top: solid #313244;
    }
    
    #tree-actions Button {
        min-width: 4;
        margin: 0 1;
    }
    
    #preview-actions {
        height: 3;
        align: center middle;
        background: #181825;
        border-top: solid #313244;
    }
    #preview-actions Button {
        margin: 0 1;
    }
    
    #dialog {
        padding: 1 2;
        width: 62;
        height: auto;
        border: thick #89dceb;
        background: #1e1e2e;
        color: #cdd6f4;
        align: center middle;
    }
    
    .large-dialog {
        width: 72;
        height: 80%;
    }
    
    #dialog-buttons {
        height: auto;
        align: right middle;
        margin-top: 1;
    }
    
    #dialog-buttons Button {
        margin-left: 1;
    }
    
    .prop-header {
        text-style: bold;
        color: #89dceb;
        margin-bottom: 1;
    }
    
    .prop-label {
        color: #f9e2af;
        margin-top: 1;
    }
    
    .mock-header {
        width: 100%;
        background: #313244;
        color: #89dceb;
        text-align: center;
    }
    
    .mock-footer {
        width: 100%;
        background: #313244;
        color: #a6adc8;
        text-align: center;
        dock: bottom;
    }
    """

    def on_mount(self):
        self.push_screen(StartScreen())

    def switch_to_editor(self, project: ProjectModel):
        self.push_screen(EditorScreen(project))

    def switch_to_start(self):
        self.pop_screen()
        if isinstance(self.screen, StartScreen):
            self.screen.refresh_projects()
