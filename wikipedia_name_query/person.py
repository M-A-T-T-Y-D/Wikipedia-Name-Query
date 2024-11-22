'''
The module is used when calculating the age of a person that is not dead
'''
from datetime import datetime
from wikipedia_name_query.query import Query



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
        self.FullName: the data collected from the query of the full name
        self.age: the calculation needed to work out the age of the person
        self.DOB: the data collected from the query of the date of birth
        self.DOD: the data collected from the query of the Date Of Death
        test
        '''



        self.name = name
        self.fullname = None
        self.age = None
        self.dob = None
        self.dod = None



    def load(self):
        '''
        This function assigns the retrived data to the variables
        '''
        x = Query()
        person_info = x.get_person_info(self.name)
        if person_info == None:
            self.fullname = None
            self.dob = None
            self.dod = None
            self.age = None
        else:
            self.fullname = person_info[0][0]
            self.dob = person_info[0][1]
            self.dod = person_info[0][2]
            age = self.calculate_age(self.dob, self.dod)
            self.age = age


    def get_fname(self):
        '''
        This function outputs the name
        '''
        full_name = self.fullname
        return full_name

    def get_dob(self):
        '''
        This function outputs the date of birth
        '''
        dob = self.dob
        return dob

    def get_dod(self):
        '''
        This function outputs the date of death
        '''
        dod = self.dod
        return dod

    def get_age(self):
        '''
        This function outputs the age
        '''
        age = self.age
        return age

    def set_fullname(self):
        '''
        This function sets the name to an input
        '''
        name = input("what would you like to set the name as")
        self.fullname = name
        return self.fullname

    def set_age(self):
        '''
        This function allows the user to set the age
        '''
        age = input("what would you like to set the age as")
        self.age = age
        return self.age

    def set_dob(self):
        '''
        This function allows the user to set the date of birth
        '''
        dob = input("what would you like to set the dob as")
        self.dob = dob
        return self.dob

    def set_dod(self):
        '''
        This function allows the user to set the date of death
        '''
        dod = input("what would you like to set the dod as")
        self.dod = dod
        return self.dod

    @staticmethod
    def calculate_age(birth_date, death_date=None,):
        '''
        This function uses datetime to get todays date then calculates 
        how many years has passed since a date to calculate age
        '''
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
        if death_date:
            death_date = datetime.strptime(death_date, "%Y-%m-%d")
            age = (death_date - birth_date).days // 365
        else:
            age = (datetime.now() - birth_date).days // 365
        return age
