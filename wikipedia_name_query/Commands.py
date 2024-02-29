import argparse
from Person import Person


def main(self):
    if args.command == 'name':
        Person(args.Name).Load()
        print(self.fullname)

    elif args.command == 'age':
        Person(args.Name).Load()
        print(self.age)

    elif args.command == 'DOB':
        Person(args.Name).Load()
        print(self.dob)

    elif args.command == 'DOD':
        Person(args.Name).Load()
        print(self.dod)

    elif args.command == 'Output':
        Person(args.Name).Load()
        print(self.fullname)
        print(self.age)
        print(self.dob)
        print(self.dod)

    elif args.command == 'setFname':
        fullname = Person(args.Name).set_fullname()
        print("you set the name to", fullname)

    elif args.command == 'setage':
        age = Person(args.age).set_age()
        print("you set age to", age)

    elif args.command == 'setdob':
        dob = Person(args.dob).set_dob()
        print("you set dob to", dob)

    elif args.command == 'setdod':
        dod = Person(args.dod).set_dod()
        print("you set dod to", dod)

    
    
        

    else:
        print('No such command please try again')
        


parser = argparse.ArgumentParser(description='Find data about someone')#creates the list of commands and their description
subparsers = parser.add_subparsers(help='commands', dest='command')


name_parser = subparsers.add_parser('name', help='Selects the person')#shortens the command 
name_parser.add_argument('--Name', type=str, default=False, help='Selects person' )


age_parser = subparsers.add_parser('age', help='Retrieves the age')
age_parser.add_argument('--Name', type=str, default=False, help='Selects person')#this command starts the code to find the persons age

DOB_parser = subparsers.add_parser('DOB', help='retrieves the date of birth')
DOB_parser.add_argument('--Name', type=str, default=False, help='Selects person ')

DOD_parser = subparsers.add_parser('DOD', help='Retreives the date of death')
DOD_parser.add_argument('--Name', type=str, default=False, help='Selects person')

Output_parser = subparsers.add_parser('Output', help='Prints the data collected about the person')
Output_parser.add_argument('--Name', type=str, default=False, help='Selects person')

setFname_parser = subparsers.add_parser('set_name', help='sets the variable for testing')
setFname_parser.add_argument('--Name', type=str, default=False, help='sets the name to the input')

setage_parser = subparsers.add_parser('set_age', help='sets the age for testing')
setage_parser.add_argument('--age', type=str, default=False, help='sets the age to input')

setdob_parser = subparsers.add_parser('set_dob', help='sets the dob for testing')
setdob_parser.add_argument('--dob', type=str, default=False, help='sets the dob to input')

setdod_parser = subparsers.add_parser('set_dod', help='sets the dod for testing')
setdod_parser.add_argument('--dod', type=str, default=False, help='sets the dod to input')

args = parser.parse_args()

if __name__ == '__main__':
    main()