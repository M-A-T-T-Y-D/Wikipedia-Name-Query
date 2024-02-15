from Query import get_person_info, calculate_age
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

def get_list(name):
    person_info = get_person_info(name)
    FullName = person_info[0][0]
    DOB = person_info[0][1]
    DOD = person_info[0][2]
    f = open("People.csv","w")
    old = open("People.csv","r")
    New = ("{} {} {} {} \n").format(old, FullName, DOB, DOD)
    f.write(New)
    f.close()
    

 