from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Grid
from textual.widgets import (
    Button, 
    Label,
)

class QuestionDialog(Screen):
    """
    Dialog for asking confirmation questions.
    """

    def __init__(self, message: str, *args, **kwargs):
        """
        Initialize the QuestionDialog.

        Parameters
        ----------
        message : str
            The confirmation message to display.
        *args
            Additional positional arguments.
        **kwargs
            Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.message = message


    def compose(self) -> ComposeResult:
        """
        Create the question dialog layout.

        Returns
        -------
        ComposeResult
            The composed UI elements for the question dialog.
        """
        no_button = Button("No", variant="primary", id="no")
        no_button.focus()

        yield Grid(
            Label(self.message, id="question"),
            Button("Yes", variant="error", id="yes"),
            no_button,
            id="question-dialog",
        )


    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Handle button presses in the QuestionDialog.

        Parameters
        ----------
        event : Button.Pressed
            The button press event.
        """
        if event.button.id == "yes":
            self.dismiss(True)
        else:
            self.dismiss(False)
    