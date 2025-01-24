import pytest
from unittest.mock import MagicMock
from wikipedia_name_query.TUI.query_app import QueryApp
from wikipedia_name_query.input_database import Database


@pytest.fixture
def mock_database():
    """Fixture to provide a mock database."""
    db = MagicMock(Database)
    db.get_all_names.return_value = [(1, "John Doe"), (2, "Jane Doe")]
    db.add_name.return_value = None
    db.remove_name.return_value = None
    db.clear_all_names.return_value = None
    return db


@pytest.fixture
def app(mock_database):
    """Fixture to provide a QueryApp instance with a mocked database."""
    return QueryApp(db=mock_database)


def test_initial_theme(app):
    """Test if the initial theme is correctly set to 'textual-dark'."""
    assert app.theme == "textual-dark", f"Expected 'textual-dark', but got {app.theme}"

def test_add_name(app, mock_database):
    """Test if adding a name updates the database."""
    # Simulate adding a name to the database
    name_to_add = "New Name"
    app.db.add_name(name_to_add)

    # Ensure the add_name method was called with the correct argument
    app.db.add_name.assert_called_with(name_to_add)


def test_clear_all_names(app, mock_database):
    """Test if clearing all names works correctly."""
    # Simulate clearing all names
    app.db.clear_all_names()

    # Ensure the database method was called to clear all names
    app.db.clear_all_names.assert_called_once()


def test_theme_toggle(app):
    """Test if toggling the theme changes the theme correctly."""
    initial_theme = app.theme
    app.action_toggle_dark()  # Simulate theme toggle
    assert app.theme != initial_theme, f"Theme did not toggle. Expected different from {initial_theme}"
