'''
Imported Modules:
Pathlib: Used in connecting to the database
SQLite3: Used to create the database and perform queries
'''
import pathlib
import sqlite3

# Define the path for the database file
DATABASE_PATH = pathlib.Path().home() / "List.db"

class Database:
    '''
    Class: Database
    This class is used to create a database and perform queries on it. 
    It allows users to add, delete, and view items in the list.
    It can be imported onto other scripts to use its functionality.
    '''
    def __init__(self, db_path=DATABASE_PATH):
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()
        self._create_table()

    def _create_table(self):
        """Create the names table if it doesn't exist."""
        query = """
            CREATE TABLE IF NOT EXISTS names(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );
        """
        self._run_query(query)

    def _run_query(self, query, *query_args):
        """Execute a query with optional arguments and commit changes."""
        try:
            result = self.cursor.execute(query, query_args)  # Pass query_args directly
            self.db.commit()
            return result
        except Exception as e:
            print(f"An error occurred while executing the query: {e}")
            return None

    def add_name(self, name):
        """Add a new name to the database."""
        if name:
            self._run_query("INSERT INTO names (name) VALUES (?);", name)
        else:
            print("Cannot add an empty name.")

    def remove_name(self, id):
        """Remove a name from the database by its ID."""
        self._run_query("DELETE FROM names WHERE id = ?;", (id,))

    def clear_all_names(self):
        """Remove all names from the database."""
        self._run_query("DELETE FROM names;")

    def get_all_names(self):
        """Retrieve all names from the database."""
        result = self._run_query("SELECT * FROM names;")
        return result.fetchall()  # Returns a list of tuples (id, name)

    def get_last_name(self):
        """Retrieve the last name added to the database"""
        result = self._run_query(
            "SELECT * FROM names ORDER BY id DESC LIMIT 1;"
        )
        return result.fetchone()

    def close(self):
        """Close the database connection."""
        self.db.close()
