from Query import get_person_info, calculate_age
class Person():
    def __init__(self, name):
        """
        This function takes the users input from the main program and calls the query 
        which returns the output

        Parameters
        -----------
        Person_info : list
            This is a list of all data collected from the query
        age : Int
            This is the calculated age of the person
        """
        self.name = name 
        self.FullName = 'None'
        self.age = 0
        self.DOB = 0
        self.DOD = 0


    def get_FullName(self):
        person_info = get_person_info(self.name)
        print(person_info[0][0]) #Runs the query to retreive the full name
        self.FullName = (person_info[0][0])
        global name
        name = self.name

    def get_DOB(self):
        person_info = get_person_info(self.name)
        print(person_info[0][0],'was born on:',person_info[0][1])
        self.DOB = (person_info[0][1])

    def get_DOD(self):
        person_info = get_person_info(self.name)
        print(person_info[0][0], person_info[0][2])
        self.DOD = (person_info[0][2])

    def get_age(self):
        person_info = get_person_info(self.name)
        age = calculate_age(person_info[0][1])
        print(person_info[0][0],'Is', age ,'Years Old')
        self.age = (age)

    

 