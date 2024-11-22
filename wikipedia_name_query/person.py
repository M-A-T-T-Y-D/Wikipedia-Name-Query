import logging
from datetime import datetime
from wikipedia_name_query.query import Query

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Configure logging
file_handler = logging.FileHandler('app.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
file_handler.flush()
logger.addHandler(file_handler)

class Person():
    '''
    This class was made so you can create multiple instances of people that you want data for
    '''
    def __init__(self, name):
        '''
        Function: Used to state the variables you want to use in the class 
        
        Parameters
        ----------
        self.name: the users input for the name
        self.fullname: the data collected from the query of the full name
        self.age: the calculation needed to work out the age of the person
        self.dob: the data collected from the query of the date of birth
        self.dod: the data collected from the query of the Date Of Death
        '''

        self.name = name
        self.fullname = None
        self.age = None
        self.dob = None
        self.dod = None

    def load(self):
        '''
        This function assigns the retrieved data to the variables
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

    def get_fname(self):
        '''
        This function outputs the name
        '''
        return self.fullname

    def get_dob(self):
        '''
        This function outputs the date of birth
        '''
        return self.dob

    def get_dod(self):
        '''
        This function outputs the date of death
        '''
        return self.dod

    def get_age(self):
        '''
        This function outputs the age
        '''
        return self.age

    def set_fullname(self):
        '''
        This function sets the name to an input
        '''
        name = input("What would you like to set the name as? ")
        self.fullname = name
        logging.debug(f"Set fullname to {self.fullname}")
        return self.fullname

    def set_age(self):
        '''
        This function allows the user to set the age
        '''
        age = input("What would you like to set the age as? ")
        self.age = age
        logging.debug(f"Set age to {self.age}")
        return self.age

    def set_dob(self):
        '''
        This function allows the user to set the date of birth
        '''
        dob = input("What would you like to set the DOB as? ")
        self.dob = dob
        logging.debug(f"Set DOB to {self.dob}")
        return self.dob

    def set_dod(self):
        '''
        This function allows the user to set the date of death
        '''
        dod = input("What would you like to set the DOD as? ")
        self.dod = dod
        logging.debug(f"Set DOD to {self.dod}")
        return self.dod

    @staticmethod
    def calculate_age(birth_date, death_date=None):
        '''
        This function uses datetime to get today's date then calculates 
        how many years have passed since a date to calculate age
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