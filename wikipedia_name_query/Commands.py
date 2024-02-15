import argparse
from Person import Person


def main1():
    if args.command == 'name':
        Person(args.Name).get_FullName()
        
    elif args.command == 'age':
        Person(args.Name).get_age()
    elif args.command == 'DOB':
        Person(args.Name).get_DOB()
    elif args.command == 'DOD':
        Person(args.Name).get_DOD()
    elif args.command == 'Output':
        Person(args.Name).get_FullName()
        Person(args.Name).get_age()
        Person(args.Name).get_DOB()
        Person(args.Name).get_DOD()
    
        

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

args = parser.parse_args()

if __name__ == '__main__':
    main1()