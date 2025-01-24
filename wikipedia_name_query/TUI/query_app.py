"""
Text User Interface (TUI) module for the Wikipedia Name Query application.

This module provides a terminal-based user interface for querying and managing
Wikipedia data about people. It uses the Textual library to create an interactive
TUI that allows users to:

- Add names to query
- View detailed information about people (birth date, death date, age)
- Delete entries
- Import names from text files
- Toggle between light and dark themes

The interface is composed of several screens and dialogs:
- QueryApp: The main application screen with a data table and control buttons
- InputDialog: Dialog for adding new names
- QuestionDialog: Dialog for confirming user actions
- OutputData: Screen for displaying detailed Wikipedia data
- FileViewScreen: Screen for selecting and importing text files

Usage:
    To run the TUI directly:
    ```
    python
    from wikipedia_name_query.TUI import QueryApp
    from wikipedia_name_query.input_database import Database

    db = Database()
    app = QueryApp(db=db)
    app.run()
    ```

Dependencies:
    - textual: For creating the TUI
    - pathlib: For file path handling
    - sys: For platform-specific operations
"""
from textual.app import App, ComposeResult, on
from textual.containers import Horizontal, Vertical
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Static,
)
from wikipedia_name_query.input_database import Database
from wikipedia_name_query.person import Person
from wikipedia_name_query.TUI.input_dialog import InputDialog
from wikipedia_name_query.TUI.question_dialog import QuestionDialog
from wikipedia_name_query.TUI.output_data import OutputData
from wikipedia_name_query.TUI.file_view_screen import FileViewScreen

class QueryApp(App):
    """
    The main application class for the query app.

    This class provides a Text User Interface (TUI) for querying and managing Wikipedia data.
    It includes functionality for adding, deleting, and viewing names, as well as theme toggling
    and file operations.

    Attributes
    ----------
    CSS_PATH : str
        Path to the CSS styling file
    BINDINGS : list
        Keyboard shortcuts for various actions
    db : Database
        Database instance for storing and retrieving data
    theme : str
        Current theme setting ("textual-dark" or "textual-light")
    """

    CSS_PATH = "tui.tcss"
    BINDINGS = [
        ("m", "toggle_dark", "Toggle dark mode"),
        ("a", "add", "Add"),
        ("d", "delete", "Delete"),
        ("c", "clear_all", "Clear All"),
        ("q", "request_quit", "Quit"),
    ]

    def __init__(self, db: Database, **kwargs):
        """
        Initialize the QueryApp.

        Parameters
        ----------
        db : Database
            Database instance for storing and retrieving data
        **kwargs
            Additional keyword arguments passed to the parent App class
        """
        super().__init__(**kwargs)
        self.db = db
        self.theme = "textual-dark"  


    def compose(self) -> ComposeResult:
        """
        Compose the screen layout with all UI elements.

        Returns
        -------
        ComposeResult
            The composed UI elements including header, footer,
            output table, and buttons panel.
        """
        yield Header()
        yield Footer()

        self.output_table = self.create_output_table()
        buttons_panel = self.create_buttons_panel()

        yield Horizontal(self.output_table, buttons_panel)


    def create_output_table(self) -> DataTable:
        """
        Create and configure the output table for displaying data.

        Creates a DataTable widget with specific styling and configuration
        for displaying the list of names and their IDs.

        Returns
        -------
        DataTable
            Configured DataTable widget with ID and Name columns
        """
        table = DataTable(classes="Output-List", id="output-table")  # Give an id to the DataTable
        table.add_columns("ID", "Name")
        table.cursor_type = "row"
        table.zebra_stripes = True
        return table


    def create_buttons_panel(self) -> Vertical:
        """
        Create and configure the buttons panel.

        Creates a vertical panel containing buttons for various operations
        like Add, Delete, View, Clear All, and File operations.

        Returns
        -------
        Vertical
            A vertical container with configured buttons
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


    def on_mount(self) -> None:
        """
        Initialize the app when mounted.

        Sets up the initial state of the application including the title,
        subtitle, and loads existing names from the database into the table.
        """
        self.title = "Wiki Query"
        self.sub_title = "An App To Query Wikipedia"
        self._load_names()


    def _load_names(self) -> None:
        """
        Load names from the database into the DataTable.

        Retrieves all names from the database and populates the DataTable,
        including error handling for invalid data formats.
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


    def action_toggle_dark(self) -> None:
        """
        Toggle between light and dark themes.

        Switches the application theme between 'textual-light' and 'textual-dark',
        and displays a notification of the current theme state.
        """
        self.theme = "textual-light" if self.theme == "textual-dark" else "textual-dark"
        self.notify(f"Theme: {self.theme}")


    @on(Button.Pressed, "#add")
    def action_add(self) -> None:
        """
        Handle the add action.

        Opens an InputDialog for adding a new name to the database and table.
        On successful addition, updates both the database and the UI table.
        """
        def check_name(name_data: str) -> None:
            if name_data:
                self.db.add_name(name_data)
                id, *name = self.db.get_last_name()
                self.query_one("#output-table").add_row(*name, key=id)
                self.notify("Name added successfully!")

        self.push_screen(InputDialog(), check_name)


    @on(Button.Pressed, "#clear")
    def action_clear_all(self) -> None:
        """
        Handle the clear all action.

        Prompts for confirmation before clearing all names from both
        the database and the UI table. Shows appropriate notifications
        for empty tables and successful clearing operations.
        """
        name_list = self.query_one("#output-table")
        if name_list.row_count == 0:
            self.notify("No names to clear!")
            return

        def check_answer(accepted: bool) -> None:
            if accepted:
                self.db.clear_all_names()
                name_list.clear()
                self.notify("All names cleared successfully!")

        self.push_screen(QuestionDialog("Are you sure you want to remove all names?"), check_answer)


    @on(Button.Pressed, "#delete")
    def action_delete(self) -> None:
        """
        Handle the delete action.

        Deletes the currently selected name from both the database and UI table
        after confirmation. Handles cases where no name is selected or the table
        is empty.
        """
        name_list = self.query_one("#output-table")

        if name_list.row_count == 0:
            self.notify("No names to delete!")
            return

        try:
            row_key, _ = name_list.coordinate_to_cell_key(name_list.cursor_coordinate)
            name = name_list.get_row(row_key)[0]

            def check_answer(accepted: bool) -> None:
                if accepted and row_key:
                    self.db.remove_name(id=row_key.value)
                    name_list.remove_row(row_key)
                    self.notify(f"Deleted name with ID {row_key.value}!")

            self.push_screen(QuestionDialog(f"Do you want to delete {name}'s?"), check_answer)
        except (IndexError, AttributeError):
            self.notify("Please select a name to delete!")


    @on(Button.Pressed, "#view")
    def action_view(self) -> None:
        """
        Handle the view action.

        Opens a detailed view of the selected name's Wikipedia data.
        Handles cases where no name is selected or the table is empty.
        """
        name_list = self.query_one("#output-table")

        if name_list.row_count == 0:
            self.notify("No names to view!")
            return

        try:
            row_key, _ = name_list.coordinate_to_cell_key(name_list.cursor_coordinate)
            name = name_list.get_row(row_key)[0]

            def check_answer(accepted: bool) -> None:
                if accepted:
                    self.push_screen(OutputData(name=name))

            self.push_screen(QuestionDialog(f"Are you sure you want to view the data for {name}?"), check_answer)
        except (IndexError, AttributeError):
            self.notify("Please select a name to view!")


    @on(Button.Pressed, "#file")
    def action_view_files(self) -> None:
        """
        Handle the file view action.

        Opens the file selection screen for importing names from a text file.
        Processes the selected file and updates both the database and UI table
        with the imported names.
        """
        def process_file_contents(file_contents: str) -> bool:
            if file_contents:
                names_added = False
                for line in file_contents.splitlines():
                    if line.strip():
                        names = [name.strip() for name in line.split(',')]
                        for name in names:
                            if name:
                                self.db.add_name(name)
                                names_added = True
                return names_added
            return False

        def after_screen_dismissed(processed: bool) -> None:
            if processed:
                self.query_one("#output-table").clear()
                self._load_names()
                self.notify("Names from file have been added to the database successfully!")

        self.push_screen(FileViewScreen(process_file_contents), after_screen_dismissed)


    def action_request_quit(self) -> None:
        """
        Handle the quit action.

        Prompts for confirmation before exiting the application.
        """
        def check_answer(accepted: bool) -> None:
            if accepted:
                self.exit()

        self.push_screen(QuestionDialog("Do you want to quit?"), check_answer)

