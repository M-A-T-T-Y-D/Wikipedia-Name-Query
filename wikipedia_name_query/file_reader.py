class NameFileReader:
    """A class to read names from a text file and output them as comma-separated values."""
    
    def __init__(self):
        """Initialize the NameFileReader and database connection."""
        self.names = []
        self.db = Database()
        
    def clear_names(self):
        """Clear the names list."""
        self.names = []
        
    def read_file(self, file_path: str) -> str:
        """
        Read names from a text file, store them in the database, and return them as comma-separated values.
        
        Args:
            file_path (str): Path to the text file containing names
            
        Returns:
            str: Comma-separated string of names
            
        Raises:
            FileNotFoundError: If the specified file does not exist
            IOError: If there is an error reading the file
        """
        try:
            # Clear existing names before reading new ones
            self.clear_names()
            
            with open(file_path, 'r', encoding='utf-8') as file:
                # Read lines and process names
                for line in file:
                    if line.strip():
                        # Split line by commas and process each name
                        names_in_line = [name.strip() for name in line.split(',')]
                        # Add each name to both the list and database
                        for name in names_in_line:
                            if name:  # Only add non-empty names
                                self.names.append(name)
                                self.db.add_name(name)
                
            # Join names with commas
            return ', '.join(self.names)
            
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {file_path} was not found")
        except IOError as e:
            raise IOError(f"Error reading file {file_path}: {str(e)}")
    
    def get_names_list(self) -> list:
        """
        Get the list of names from the last read file.
        
        Returns:
            list: List of names
        """
        return self.names
    
    def close(self):
        """Close the database connection."""
        if hasattr(self, 'db'):
            self.db.close()
