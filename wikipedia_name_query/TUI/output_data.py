from textual.screen import Screen
from textual.containers import Vertical
from textual.app import ComposeResult
from textual.widgets import (
    Button,
    Label,
    Static,
)
from wikipedia_name_query.person import Person

class OutputData(Screen):
    """
    Screen to display detailed data for a selected name.
    """

    def __init__(self, name: str, *args, **kwargs):
        """
        Initialize the OutputData screen.

        Parameters
        ----------
        name : str
            The name of the person to display data for.
        *args
            Additional positional arguments.
        **kwargs
            Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.person_name = name
        self.person_query = Person(self.person_name)
        self.person_query.load()


    def compose(self) -> ComposeResult:
        """
        Create the output data screen layout.

        Returns
        -------
        ComposeResult
            The composed UI elements for the output data screen.
        """
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
            id="output-screen"
        )


    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Handle button presses in the OutputData screen.

        Parameters
        ----------
        event : Button.Pressed
            The button press event.
        """
        if event.button.id == "ok":
            self.dismiss()