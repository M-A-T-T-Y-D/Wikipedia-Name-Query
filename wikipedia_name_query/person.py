import logging
from datetime import datetime
from wikipedia_name_query.query import Query

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('app.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
file_handler.flush()
logger.addHandler(file_handler)


class Person:
    """
    A class to represent an individual and retrieve, manage, and manipulate their data.

    Attributes
    ----------
    name : str
        The identifier for the person.
    fullname : str or None
        The full name of the person.
    age : int or None
        The age of the person.
    dob : str or None
        The date of birth of the person (format: YYYY-MM-DD).
    dod : str or None
        The date of death of the person (format: YYYY-MM-DD).
    """

    def __init__(self, name: str) -> None:
        '''
        Initializes a Person instance.

        Parameters
        ----------
        name : str
            The name or identifier for the person.
        '''
        self.name = name
        self.fullname = None
        self.age = None
        self.dob = None
        self.dod = None

    def load(self) -> dict | None:
        '''
        Loads the person's data using the `Query` interface and assigns it to instance attributes.
        
        Returns
        -------
        person_info : dict or None
            The data retrieved for the person. None if no data is found.
        '''
        logging.debug(f"Loading data for {self.name}")
        x = Query()
        person_info = x.get_person_info(self.name)

        if person_info is None:
            self.fullname = None
            self.dob = None
            self.dod = None
            self.age = None
            logging.debug(f"No information found for {self.name}")
        else:
            self.fullname = person_info[0][0]
            self.dob = person_info[0][1]
            self.dod = person_info[0][2]
            self.age = self.calculate_age(self.dob, self.dod)
            logging.debug(f"Loaded data for {self.fullname}: DOB={self.dob}, DOD={self.dod}, Age={self.age}")
        
        return person_info

    def get_fname(self) -> str | None:
        '''
        Returns the person's full name.

        Returns
        -------
        fullname : str or None
            The full name of the person, or None if not available.
        '''
        return self.fullname

    def get_dob(self) -> str | None:
        '''
        Returns the person's date of birth.

        Returns
        -------
        dob : str or None
            The date of birth in the format YYYY-MM-DD, or None if not available.
        '''
        return self.dob

    def get_dod(self) -> str | None:
        '''
        Returns the person's date of death.

        Returns
        -------
        dod : str or None
            The date of death in the format YYYY-MM-DD, or None if not available.
        '''
        return self.dod

    def get_age(self) -> int | None:
        '''
        Returns the person's age.

        Returns
        -------
        age : int or None
            The person's age, or None if not available.
        '''
        return self.age

    def set_fullname(self) -> str:
        '''
        Prompts the user to set a new full name for the person.

        Returns
        -------
        fullname : str
            The new full name entered by the user.
        '''
        name = input("What would you like to set the name as? ")
        self.fullname = name
        logging.debug(f"Set fullname to {self.fullname}")
        return self.fullname

    def set_age(self) -> int:
        '''
        Prompts the user to set a new age for the person.

        Returns
        -------
        age : int
            The new age entered by the user.
        '''
        age = input("What would you like to set the age as? ")
        self.age = int(age)
        logging.debug(f"Set age to {self.age}")
        return self.age

    def set_dob(self) -> str:
        '''
        Prompts the user to set a new date of birth for the person.

        Returns
        -------
        dob : str
            The new date of birth entered by the user (format: YYYY-MM-DD).
        '''
        dob = input("What would you like to set the DOB as? ")
        self.dob = dob
        logging.debug(f"Set DOB to {self.dob}")
        return self.dob

    def set_dod(self) -> str:
        '''
        Prompts the user to set a new date of death for the person.

        Returns
        -------
        dod : str
            The new date of death entered by the user (format: YYYY-MM-DD).
        '''
        dod = input("What would you like to set the DOD as? ")
        self.dod = dod
        logging.debug(f"Set DOD to {self.dod}")
        return self.dod

    @staticmethod
    def calculate_age(birth_date: str, death_date: str | None = None) -> int:
        '''
        Calculates the person's age based on their birth date and optionally their death date.
        
        Parameters
        ----------
        birth_date : str
            The person's date of birth in the format YYYY-MM-DD.
        death_date : str, optional
            The person's date of death in the format YYYY-MM-DD. Defaults to None.
        
        Returns
        -------
        age : int
            The calculated age in years.
        
        Raises
        ------
        ValueError
            If the date format is invalid or the birth date is in the future.
        '''
        logging.debug(f"Calculating age for birth_date={birth_date}, death_date={death_date}")
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
        
        if death_date:
            death_date = datetime.strptime(death_date, "%Y-%m-%d")
            age = (death_date - birth_date).days // 365
        else:
            age = (datetime.now() - birth_date).days // 365
        
        logging.debug(f"Calculated age: {age}")
        return age
