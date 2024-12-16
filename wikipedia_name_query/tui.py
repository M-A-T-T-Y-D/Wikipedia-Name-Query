import sys
from pathlib import Path
from textual.app import App, ComposeResult, on
from textual.containers import Grid, Horizontal, Vertical, VerticalScroll, Container
from textual.reactive import reactive
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
from wikipedia_name_query.input_database import Database
from wikipedia_name_query.person import Person

class QueryApp(App):
    """The main application class for the query app."""
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

    def compose(self):
        """Composes the screen layout."""
        yield Header()
        yield Footer()

        self.output_table = self.create_output_table()
        buttons_panel = self.create_buttons_panel()

        yield Horizontal(self.output_table, buttons_panel)

    def create_output_table(self) -> DataTable:
        """
        Creates the output table to display the data collected.
        """
        table = DataTable(classes="Output-List", id="output-table")  # Give an id to the DataTable
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

    def on_mount(self):
        """Loads the screen and retrieves data to load onto the table."""
        self.title = "Wiki Query"
        self.sub_title = "An App To Query Wikipedia"
        self._load_names()

    def _load_names(self):
        """
        Loads the names from the database and adds them to the DataTable.
        """
        name_list = self.query_one("#output-table")  # Reference by id
        for name_data in self.db.get_all_names():
            if isinstance(name_data, tuple) and len(name_data) == 2:
                id, name = name_data
                if isinstance(name, str) and name.strip():
                    name_list.add_row(name, key=id)
                else:
                    self.notify(f"Invalid name data: {name_data}")
            else:
                self.notify(f"Invalid data format: {name_data}")



    @on(Button.Pressed, "#add")
    def action_add(self):
        """Adds a name to the table."""
        def check_name(name_data):
            if name_data:
                self.db.add_name(name_data)
                id, *name = self.db.get_last_name()
                self.query_one("#output-table").add_row(*name, key=id)  # Add to the correct DataTable
                self.notify("Name added successfully!")

        self.push_screen(InputDialog(), check_name)

    @on(Button.Pressed, "#clear")
    def action_clear_all(self):
        """Clears all names from the table."""
        def check_answer(accepted):
            if accepted:
                self.db.clear_all_names()
                self.query_one("#output-table").clear()
                self.notify("All names cleared successfully!")

        self.push_screen(QuestionDialog("Are you sure you want to remove all names?"), check_answer)

    @on(Button.Pressed, "#delete")
    def action_delete(self):
        """Deletes names from the output table."""
        name_list = self.query_one("#output-table")
        row_key, _ = name_list.coordinate_to_cell_key(name_list.cursor_coordinate)

        def check_answer(accepted):
            if accepted and row_key:
                self.db.remove_name(id=row_key.value)
                name_list.remove_row(row_key)
                self.notify(f"Deleted name with ID {row_key.value}!")

        name = name_list.get_row(row_key)[0]
        self.push_screen(QuestionDialog(f"Do you want to delete {name}'s?"), check_answer)

    @on(Button.Pressed, "#view")
    def action_view(self):
        """Views the collected data on the selected name."""
        name_list = self.query_one("#output-table")
        row_key, _ = name_list.coordinate_to_cell_key(name_list.cursor_coordinate)
        name = name_list.get_row(row_key)[0]

        def check_answer(accepted):
            if accepted:
                self.push_screen(OutputData(name=name))

        self.push_screen(QuestionDialog(f"Are you sure you want to view the data for {name}?"), check_answer)

    @on(Button.Pressed, "#file")
    def action_view_files(self):
        """Opens the file view screen."""
        def process_file_contents(file_contents: str):
            if file_contents:
                names_added = False
                for line in file_contents.splitlines():
                    if line.strip():
                        # Split line by commas and process each name
                        names = [name.strip() for name in line.split(',')]
                        for name in names:
                            if name:  # Only add non-empty names
                                self.db.add_name(name)
                                names_added = True
                return names_added
            return False

        def after_screen_dismissed(processed: bool):
            if processed:
                self.query_one("#output-table").clear()  # Clear the table
                self._load_names()  # Reload names into the table
                self.notify("Names from file have been added to the database successfully!")

        self.push_screen(FileViewScreen(process_file_contents), after_screen_dismissed)

    def action_toggle_dark(self):
        """Toggles Dark mode."""
        self.dark = not self.dark

    def action_request_quit(self):
        """Lets the user terminate the terminal."""
        def check_answer(accepted):
            if accepted:
                self.exit()

        self.push_screen(QuestionDialog("Do you want to quit?"), check_answer)


class InputDialog(Screen):
    """Dialog for adding a name."""
    def compose(self):
        yield Grid(
            Label("Add name", id="title"),
            Label("Name:", classes="label"),
            Input(
                placeholder="Name",
                classes="input",
                id="name",
            ),
            Static(),
            Button("Cancel", variant="warning", id="cancel"),
            Button("Ok", variant="success", id="ok"),
            id="input-dialog",
        )

    def on_button_pressed(self, event):
        """Handles button presses in the InputDialog."""
        if event.button.id == "ok":
            name = self.query_one("#name").value
            if name and isinstance(name, str):  # Ensure it's a non-empty string
                self.dismiss(name)
            else:
                self.dismiss()
        else:
            self.dismiss()



class QuestionDialog(Screen):
    """Dialog for asking confirmation questions."""
    def __init__(self, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message

    def compose(self):
        no_button = Button("No", variant="primary", id="no")
        no_button.focus()

        yield Grid(
            Label(self.message, id="question"),
            Button("Yes", variant="error", id="yes"),
            no_button,
            id="question-dialog",
        )

    def on_button_pressed(self, event):
        """Handles button presses in the QuestionDialog."""
        if event.button.id == "yes":
            self.dismiss(True)
        else:
            self.dismiss(False)


class OutputData(Screen):
    """Screen to display detailed data for a selected name."""
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.person_name = name
        self.person_query = Person(self.person_name)
        self.person_query.load()

    def compose(self):
        yield Vertical(
            Label("Output", id="output-title"),
            Label(f"Name: {self.person_query.fullname}", classes="output-label"),
            Static(),
            Label(f"Date of Birth: {self.person_query.dob}", classes="output-label"),
            Static(),
            Label(f"Date of Death: {self.person_query.dod}", classes="output-label"),
            Static(),
            Label(f"Age: {self.person_query.age}", classes="output-label"),
            Static(),
            Button("Ok", variant="success", id="ok"),
            Static(),
            Button("Edit", variant="warning", id="edit"),
            id="output-screen"
        )

    def on_button_pressed(self, event):
        """Handles button presses in the OutputData screen."""
        if event.button.id == "ok":
            self.dismiss()


class FileViewScreen(Screen):
    """Screen to select a file from the system."""
    CSS_PATH = "File.tcss"
    path: reactive[str | None] = reactive(None)
    selected_file: reactive[str | None] = reactive(None)
    process_file_contents: callable = None  # Function to process file contents once selected

    def __init__(self, process_file_contents: callable):
        super().__init__()
        self.process_file_contents = process_file_contents
        self.processed = False

    def compose(self):
        """Composes the UI for file selection."""
        if sys.platform == "win32":
            path = "C:\\"  
        else:
            path = "/"  
        self.path = path

        yield Header()
        yield DirectoryTree(path, id="tree-view")
        yield Button("Confirm Selection", id="confirm-button")
        yield Button("Clear Selection", id="clear-button")
        yield Footer()

    def on_mount(self) -> None:
        """Focus the directory tree on mount."""
        tree = self.query_one(DirectoryTree)
        tree.focus()

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """Handle when a file is selected in the DirectoryTree."""
        file_path = event.path
        if file_path.is_file() and file_path.suffix == ".txt":
            self.selected_file = str(file_path)
            self.notify(f"Selected file: {file_path}")
        else:
            self.selected_file = None
            self.notify("Only text files can be selected.")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "confirm-button":
            if self.selected_file:
                with open(self.selected_file, "r") as file:
                    file_contents = file.read()
                    self.processed = self.process_file_contents(file_contents)
                self.dismiss(self.processed)  # Close screen after confirming, passing processed status
            else:
                self.notify("Please select a valid text file first!")
        elif event.button.id == "clear-button":
            self.selected_file = None
            self.notify("File selection cleared.")


if __name__ == "__main__":
    db = Database()
    app = QueryApp(db=db)
    app.run()
