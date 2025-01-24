from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Grid
from textual.widgets import (
    Button,
    Input,
    Label,
    Static,
)

class InputDialog(Screen):
    """
    Dialog for adding a name.
    """

    def compose(self) -> ComposeResult:
        """
        Create the input dialog layout.

        Returns
        -------
        ComposeResult
            The composed UI elements for the input dialog.
        """
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


    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Handle button presses in the InputDialog.

        Parameters
        ----------
        event : Button.Pressed
            The button press event.
        """
        if event.button.id == "ok":
            name = self.query_one("#name").value
            if name and isinstance(name, str):
                self.dismiss(name)
            else:
                self.dismiss()
        else:
            self.dismiss()