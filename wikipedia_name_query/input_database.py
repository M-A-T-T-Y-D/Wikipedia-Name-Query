'''
Imported Modules:
- Pathlib: Used in connecting to the database.
- SQLite3: Used to create the database and perform queries.
'''
import pathlib
import sqlite3

DATABASE_PATH = pathlib.Path().home() / "List.db"


class Database:
    '''
    A class to create and manage a SQLite database. 

    This class allows users to perform operations such as adding, deleting,
    and viewing items in a database table. It can also be imported into other
    scripts for its functionality.

    Attributes
    ----------
    db : sqlite3.Connection
        A connection object to the SQLite database.
    cursor : sqlite3.Cursor
        A cursor object to execute database queries.
    '''

    def __init__(self, db_path: str = DATABASE_PATH) -> None:
        '''
        Initializes the database connection and ensures the table is created.

        Parameters
        ----------
        db_path : str, optional
            The path to the SQLite database file. Defaults to `DATABASE_PATH`.
        '''
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()
        self._create_table()

    def _create_table(self) -> None:
        '''
        Creates the `names` table if it doesn't already exist.

        The table contains the following columns:
        - id : INTEGER (Primary Key)
        - name : TEXT (Non-Null)
        '''
        query = """
            CREATE TABLE IF NOT EXISTS names(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );
        """
        self._run_query(query)

    def _run_query(self, query: str, *query_args) -> sqlite3.Cursor | None:
        '''
        Executes a query with optional arguments and commits the changes.

        Parameters
        ----------
        query : str
            The SQL query to execute.
        query_args : tuple
            Optional arguments for the SQL query.

        Returns
        -------
        sqlite3.Cursor or None
            The result of the executed query. Returns None if an error occurs.
        '''
        try:
            result = self.cursor.execute(query, query_args)
            self.db.commit()
            return result
        except Exception as e:
            print(f"An error occurred while executing the query: {e}")
            return None

    def add_name(self, name: str) -> None:
        '''
        Adds a new name to the `names` table.

        Parameters
        ----------
        name : str
            The name to be added to the database.
        '''
        if name:
            self._run_query("INSERT INTO names (name) VALUES (?);", name)
        else:
            print("Cannot add an empty name.")

    def remove_name(self, id: int) -> None:
        '''
        Removes a name from the `names` table by its ID.

        Parameters
        ----------
        id : int
            The ID of the name to be removed.
        '''
        self._run_query("DELETE FROM names WHERE id = ?;", (id,))

    def clear_all_names(self) -> None:
        '''
        Removes all names from the `names` table.
        '''
        self._run_query("DELETE FROM names;")

    def get_all_names(self) -> list[tuple[int, str]]:
        '''
        Retrieves all names from the `names` table.

        Returns
        -------
        list of tuple
            A list of tuples, where each tuple contains:
            - id (int): The ID of the name.
            - name (str): The name.
        '''
        result = self._run_query("SELECT * FROM names;")
        return result.fetchall() if result else []

    def get_last_name(self) -> tuple[int, str] | None:
        '''
        Retrieves the last name added to the `names` table.

        Returns
        -------
        tuple or None
            A tuple containing:
            - id (int): The ID of the name.
            - name (str): The name.
            Returns None if the table is empty.
        '''
        result = self._run_query(
            "SELECT * FROM names ORDER BY id DESC LIMIT 1;"
        )
        return result.fetchone() if result else None

    def close(self) -> None:
        '''
        Closes the database connection.
        '''
        self.db.close()
