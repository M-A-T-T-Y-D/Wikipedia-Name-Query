import sys
from typing import Callable
from textual.screen import Screen
from textual.reactive import reactive
from textual.app import ComposeResult
from textual.widgets import (
    Button,
    DirectoryTree,
    Footer,
    Header,
)
from wikipedia_name_query.person import Person

class FileViewScreen(Screen):
    """
    Screen to select a file from the system.
    """

    CSS_PATH = "TUI.tcss"
    path: reactive[str | None] = reactive(None)
    selected_file: reactive[str | None] = reactive(None)
    process_file_contents: callable = None

    def __init__(self, process_file_contents: Callable[[str], bool]):
        """
        Initialize the FileViewScreen.

        Parameters
        ----------
        process_file_contents : Callable[[str], bool]
            A function to process the contents of the selected file.
        """
        super().__init__()
        self.process_file_contents = process_file_contents
        self.processed = False


    def compose(self) -> ComposeResult:
        """
        Create the file selection screen layout.

        Returns
        -------
        ComposeResult
            The composed UI elements for the file selection screen.
        """
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
        """
        Focus the directory tree on mount.
        """
        tree = self.query_one(DirectoryTree)
        tree.focus()


    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """
        Handle when a file is selected in the DirectoryTree.

        Parameters
        ----------
        event : DirectoryTree.FileSelected
            The file selection event containing the selected file path.
        """
        file_path = event.path
        if file_path.is_file() and file_path.suffix == ".txt":
            self.selected_file = str(file_path)
            self.notify(f"Selected file: {file_path}")
        else:
            self.selected_file = None
            self.notify("Only text files can be selected.")


    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Handle button presses in the file selection screen.

        Parameters
        ----------
        event : Button.Pressed
            The button press event containing the ID of the pressed button.
        """
        if event.button.id == "confirm-button":
            if self.selected_file:
                with open(self.selected_file, "r") as file:
                    file_contents = file.read()
                    self.processed = self.process_file_contents(file_contents)
                self.dismiss(self.processed)
            else:
                self.notify("Please select a valid text file first!")
        elif event.button.id == "clear-button":
            self.selected_file = None
            self.notify("File selection cleared.")