# Wikipedia Name Query

A Python application that retrieves biographical information about people from Wikipedia, including their full name, date of birth, date of death, and age. The application provides both a Text User Interface (TUI) and Command Line Interface (CLI) for easy interaction.

## Features

- Query Wikipedia for biographical information
- Interactive Text User Interface (TUI)
- Command Line Interface (CLI)
- Local database storage for queried names
- Support for both individual queries and batch processing
- Dark/Light theme toggle in TUI

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Wikipedia-Name-Query.git
cd Wikipedia-Name-Query
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Text User Interface (TUI)

The TUI provides an interactive interface with the following features:

1. Launch the TUI:
```bash
python -m wikipedia_name_query
```
2. Or:
```bash
Textual run tui.py
```

2. Interface Features:
- Add names using the "Add" button or 'a' key
- View detailed information with the "View" button
- Delete entries using the "Delete" button or 'd' key
- Clear all entries using the "Clear All" button or 'c' key
- Toggle dark/light theme with 'm' key
- Import names from text files using the "File" button
- Quit the application using 'q' key

### Command Line Interface (CLI)

The CLI provides direct command access for quick queries:

1. View all available commands:
```bash
python -m wikipedia_name_query -h
```

2. Query specific information:

- Get person's age:
```bash
python -m wikipedia_name_query age --Name "Albert Einstein"
```

- Get full name:
```bash
python -m wikipedia_name_query name --Name "Albert Einstein"
```

- Get date of birth:
```bash
python -m wikipedia_name_query DOB --Name "Albert Einstein"
```

- Get date of death:
```bash
python -m wikipedia_name_query DOD --Name "Albert Einstein"
```

- Get all information:
```bash
python -m wikipedia_name_query Output --Name "Albert Einstein"
```

### Example Output

```
Name: Albert Einstein
Age: 76 Years
Date of Birth: 1879-03-14
Date of Death: 1955-04-18
```

## Batch Processing

You can import multiple names at once using a text file:

1. Create a text file with names (comma-separated)
2. In the TUI, click the "File" button
3. Select your text file
4. Confirm the selection to import all names

## Development

### Running Tests

```bash
pip install -r requirements-test.txt
pytest
```

### Code Linting

```bash
python lint.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

For support, please open an issue in the GitHub repository.
