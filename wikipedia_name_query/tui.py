"""
Imported Modules:
- Textual widgets + screen + container + App: 
    The Textual library is used for creating the graphical
    user interfaces, The widgets are used to form buttons and
    visuals on the User interface, The screen is used to display
    a new window, The container is used to organize the widgets
- Person class:
    The Person class is used to call the query based of the input
    from the user, The class is used to create a new instance of
    the person object to store the data collected.
- Database Class: 
    The Database class is used to connect to the database,
    allowing the querys from the UI to be stored when the
    user terminates the program. It also loads old
    data from the database onto the display tabel.
"""
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
)
from input_database import Database
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
    ]

    def __init__(self, db: Database, **kwargs):
        super().__init__(**kwargs)
        self.db = db

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

        buttons_panel = Vertical(
            add_button,
            delete_button,
            view_button,
            Static(classes="separator"),
            clear_button,
            classes="buttons-panel",
        )
        return buttons_panel

    def on_mount(self):
        """
        Loads the screen + retreives data to load onto tabel
        """
        self.title = "Wiki Query"
        self.sub_title = "An App To Query Wikipedia"
        self._load_names()

    @on(Button.Pressed, "#add")
    def action_add(self):
        """
        Adds a name to the tabel
        """
        def check_name(name_data):
            if name_data:
                self.db.add_name(name_data)
                id, *name = self.db.get_last_name()
                self.query_one(DataTable).add_row(*name, key=id)

        self.push_screen(InputDialog(), check_name)

    @on(Button.Pressed, "#clear")
    def action_clear_all(self):
        """
        Clears all names from the tabel
        """
        def check_answer(accepted):
            if accepted:
                self.db.clear_all_names()
                self.query_one(DataTable).clear()

        self.push_screen(
            QuestionDialog("Are you sure you want to remove all names?"),
            check_answer,
        )

    @on(Button.Pressed, "#delete")
    def action_delete(self):
        """
        Deletes names of the output tabel
        """
        name_list = self.query_one(DataTable)
        row_key, _ = name_list.coordinate_to_cell_key(name_list.cursor_coordinate)

        def check_answer(accepted):
            if accepted and row_key:
                self.db.remove_name(id=row_key.value)
                name_list.remove_row(row_key)

        name = name_list.get_row(row_key)[0]
        self.push_screen(
            QuestionDialog(f"Do you want to delete {name}'s?"),
            check_answer,
        )

    @on(Button.Pressed, "#view")
    def action_view(self):
        """
        Views the collected data on the selected name
        """
        name_list = self.query_one(DataTable)
        row_key, _ = name_list.coordinate_to_cell_key(name_list.cursor_coordinate)
        name = name_list.get_row(row_key)[0]

        def check_answer(accepted):
            if accepted:
                self.push_screen(OutputData(name=name))

        self.push_screen(
            QuestionDialog(f"Are you sure you want to view the data for {name}?"),
            check_answer
        )

    def _load_names(self):
        """
        Loads the names
        """
        name_list = self.query_one(DataTable)
        for name_data in self.db.get_all_names():
            id, *name = name_data
            name_list.add_row(*name, key=id)

    def action_toggle_dark(self):
        """
        Toggles Dark mode
        """
        self.dark = not self.dark

    def action_request_quit(self):
        """
        Lets the user terminate the terminal
        """
        def check_answer(accepted):
            if accepted:
                self.exit()

        self.push_screen(QuestionDialog("Do you want to quit?"), check_answer)

class InputDialog(Screen):
    """
    This class creates the screen that verifys the users decision
    """
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
        """
        Checks the users validates the button press
        """
        if event.button.id == "ok":
            name = self.query_one("#name", Input).value
            if isinstance(name, str):
                self.dismiss(name)
            else:
                self.dismiss()
        else:
            self.dismiss()

class QuestionDialog(Screen):
    """
    This class creates the reusable screen for questions and verifying the users decision
    """
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
        """
        Checks if the user validated their input
        """
        if event.button.id == "yes":
            self.dismiss(True)
        else:
            self.dismiss(False)

class OutputData(Screen):
    """
    Class that outputs data from the selected name
    """
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
        """
        Validates the users input
        """
        if event.button.id == "yes":
            self.dismiss(True)
        else:
            self.dismiss(False)


if __name__ == "__main__":
    app = QueryApp(db=Database())
    app.run()
