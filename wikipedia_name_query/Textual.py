from textual.app import App, ComposeResult
from textual import on
from textual.widgets import Button, Input, Label, Static, Footer
from wikipedia_name_query.person import Person


class AppendTextLabel(Label):
    def __init__(self, text: str, *args, **kwargs) -> None:
        self.text = text
        super().__init__(text, *args, **kwargs)

    def append(self, text: str) -> None:
        self.text += text
        self.update(self.text)


class Panel(App):
    CSS_PATH = "Textual.tcss"
    BINDINGS =[("d", "toggle_dark", "Toggle Dark Mode")]
    def compose(self) -> ComposeResult:
        yield Output(id="output")
        yield Container(id="container")
        yield Footer()
    def on_button_pressed(self, event: Button.Pressed) -> None:
        input_user = self.query_one(Input)
        name = input_user.value
        query_name = Person(name)
        query_name.load()
        button_id = event.button.id
        if query_name.dod == None:
            query_name.dod = "Not Dead"
        if button_id == "name":
            if name_click == True:
                if query_name.fullname == None:
                    self.query_one("#results", AppendTextLabel).append("\nNo data was retrived")
                    name_click = False
                else:
                    self.query_one("#results", AppendTextLabel).append(f"\nTheir full name is : {query_name.fullname}")
                    name_click = False 
        elif button_id == "age":
            age_click = True
            if query_name.age == None:
                self.query_one("#results", AppendTextLabel).append("\nNo data was retrived")
            else:
                self.query_one("#results", AppendTextLabel).append(f"\nThey are {str(query_name.age)} years old")
        elif button_id == "birth":
            birth_click = True
            if query_name.dob == None:
                self.query_one("#results", AppendTextLabel).append("\nNo data was retrived")
            else:
                self.query_one("#results", AppendTextLabel).append(f"\nThey were born on : {query_name.dob}")
        elif button_id == "death":
            death_click = True
            if query_name.dod == None:
                self.query_one("#results", AppendTextLabel).append("\nNo data was retrived")
            else:
                self.query_one("#results", AppendTextLabel).append(f"\nThey died on : {query_name.dod}")
        
                    
    def action_toggle_dark(self):
        self.dark = not self.dark
class Container(Static):
    '''A Container widget to hold my buttons'''

    def compose(self):
        yield Input(placeholder="Enter a Name")
        yield Button("Name" ,id="name")
        yield Button("Age", id="age")
        yield Button("DOB", id="birth")
        yield Button("DoD", id="death")
        yield Button("Load",id ='load')
class Output(Static):

    def compose(self):
        yield AppendTextLabel("Output", id="results")

if __name__ == "__main__":
    app = Panel()
    app.run()
