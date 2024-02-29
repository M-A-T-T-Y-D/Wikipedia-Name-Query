from Query import Query
from Commands import *


class Person():
    def __init__(self,):
        '''
        Function: Used to state the variables you want to use in the class 
        self.name: the users input for the name
        self.FullName: the data collected from the query of the full name
        self.age: the calculation needed to work out the age of the person
        self.DOB: the data collected from the query of the date of birth
        self.DOD: the data collected from the query of the Date Of Death
        
        '''



        self.name = None 
        self.fullname = None
        self.age = None
        self.dob = None
        self.dod = None

    def Load(self):
        self.name = args.Name
        x = Query()
        person_info = x.get_person_info(self.name)
        self.fullname = person_info[0][1]
        self.dob = person_info[0][1]
        self.dod = person_info[0][2]
        age = x.calculate_age(person_info[0][1])
        self.age = age
        return self.fullname, self.dob, self.dod, self.age




