from textual.app import App, on
from textual.containers import Grid, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Input,
    Label,
    Static,
    DirectoryTree,
)
from input_database import Database
from wikipedia_name_query.person import Person


class FileViewScreen(Screen):
    """
    This class creates the screen to display the directory tree.
    """
    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = path
        self.selected_file = None  # To store the selected file

    def compose(self):
        yield Vertical(
            Label("File Browser", id="title"),
            DirectoryTree(self.path, id="directory-tree"),
        )

    def on_directory_tree_file_selected(self, event):
        """
        Handles the file selection event in the DirectoryTree.
        """
        self.selected_file = event.path
        self.app.pop_screen()  # Return to the previous screen
        self.app.handle_file_selected(self.selected_file)  # Notify the main app


class QueryApp(App):
    """
    The main application class for the query app.
    """
    CSS_PATH = "tui.tcss"
    BINDINGS = [
        ("m", "toggle_dark", "Toggle dark mode"),
        ("a", "add", "Add"),
        ("d", "delete", "Delete"),
        ("c", "clear_all", "Clear All"),
        ("q", "request_quit", "Quit"),
        ("f", "view_files", "View Files"),
    ]

    def __init__(self, db: Database, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.selected_file = None  # To store the selected file globally

    def compose(self):
        yield Header()
        yield Footer()

        self.output_table = self.create_output_table()
        buttons_panel = self.create_buttons_panel()

        yield Horizontal(self.output_table, buttons_panel)

    def create_output_table(self) -> DataTable:
        """
        Creates the output table to display the data collected.
        """
        table = DataTable(classes="Output-List")
        table.add_columns("ID", "Name")
        table.cursor_type = "row"
        table.zebra_stripes = True
        return table

    def create_buttons_panel(self) -> Vertical:
        """
        Create the buttons panel
        """
        add_button = Button("Add", variant="success", id="add")
        delete_button = Button("Delete", variant="primary", id="delete")
        view_button = Button("View", variant="warning", id="view")
        clear_button = Button("Clear All", variant="error", id="clear")
        file_button = Button("File", variant="error", id="file")

        buttons_panel = Vertical(
            add_button,
            delete_button,
            view_button,
            Static(classes="separator"),
            clear_button,
            file_button,
            classes="buttons-panel",
        )
        return buttons_panel

    @on(Button.Pressed, "#file")
    def action_view_files(self):
        """
        Opens the file view screen.
        """
        self.push_screen(FileViewScreen(path="."))  # "." for current directory

    def handle_file_selected(self, file_path):
        """
        Handles the file selected from the DirectoryTree.
        """
        self.selected_file = file_path
        self.log(f"File selected: {self.selected_file}")  # Log the selected file
        # Additional logic can be added here, e.g., displaying the file or processing it.


if __name__ == "__main__":
    app = QueryApp(db=Database())
    app.run()

