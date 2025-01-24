from wikipedia_name_query.TUI.query_app import QueryApp
from wikipedia_name_query.input_database import Database

def main():
    db = Database()
    app = QueryApp(db=db)
    app.run()

if __name__ == "__main__":
    main()