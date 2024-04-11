from datetime import datetime
from wikipedia_name_query.Query import Query



class Person():
    def __init__(self, name):
        '''
        Function: Used to state the variables you want to use in the class 
        self.name: the users input for the name
        self.FullName: the data collected from the query of the full name
        self.age: the calculation needed to work out the age of the person
        self.DOB: the data collected from the query of the date of birth
        self.DOD: the data collected from the query of the Date Of Death
        
        '''



        self.name = name
        self.fullname = None
        self.age = None
        self.dob = None
        self.dod = None



    def load(self):
        x = Query()
        person_info = x.get_person_info(self.name)
        self.fullname = person_info[0][0]
        self.dob = person_info[0][1]
        self.dod = person_info[0][2]
        age = self.calculate_age(self.dob, self.dod)
        self.age = age


    def get_fname(self):
        full_name = self.fullname
        return full_name

    def get_dob(self):
        dob = self.dob
        return dob

    def get_dod(self):
        dod = self.dod
        return dod

    def get_age(self):
        age = self.age
        return age

    def set_fullname(self):
        name = input("what would you like to set the name as")
        self.fullname = name
        return self.fullname

    def set_age(self):
        age = input("what would you like to set the age as")
        self.age = age
        return self.age

    def set_dob(self):
        dob = input("what would you like to set the dob as")
        self.dob = dob
        return self.dob

    def set_dod(self):
        dod = input("what would you like to set the dod as")
        self.dod = dod
        return self.dod

    @staticmethod
    def calculate_age(birth_date, death_date=None,):
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
        if death_date:
            death_date = datetime.strptime(death_date, "%Y-%m-%d")
            age = (death_date - birth_date).days // 365
        else:
            age = (datetime.now() - birth_date).days // 365
        return age
