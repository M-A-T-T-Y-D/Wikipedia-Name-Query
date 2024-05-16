from textual.app import App, ComposeResult
from textual import on
from textual.widgets import Button, Header, Input, Label
from wikipedia_name_query.person import Person




class Panel(App):
    CSS_PATH = "Textual.tcss"
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Input(placeholder="Enter a Name")
        yield Label(id="results")
        yield Button("Name" ,id="name")
        yield Button("Age", id="age")
        yield Button("DOB", id="birth")
        yield Button("DoD", id="death")
        yield Button("Theme", id="dark")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        input = self.query_one(Input)
        name = input.value
        query_name = Person(name)
        query_name.load()
        button_id = event.button.id
        if query_name.dod == None:
            query_name.dod = "Not Dead"
        if button_id == "name":
            self.query_one("#results", Label).update(f"Their full name is : {query_name.fullname}")
        elif button_id == "age":
            self.query_one("#results", Label).update(f"They are {str(query_name.age)} years old")
        elif button_id == "birth":
            self.query_one("#results", Label).update(f"They were born on : {query_name.dob}")
        elif button_id == "death":
            self.query_one("#results", Label).update(f"They died on : {query_name.dod}")
        elif button_id == "dark":
            self.dark = not self.dark



if __name__ == "__main__":
    app = Panel()
    app.run()
