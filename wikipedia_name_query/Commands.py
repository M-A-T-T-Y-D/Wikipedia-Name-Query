import argparse
from wikipedia_name_query.Person import Person


class Commands():
    def commands(self):
        parser = argparse.ArgumentParser(description='Find data about someone')#creates the list of commands and their description
        subparsers = parser.add_subparsers(help='commands', dest='command')


        name_parser = subparsers.add_parser('name', help='Selects the person')#shortens the command 
        name_parser.add_argument('--Name', type=str, default=False, help='Selects person' )


        age_parser = subparsers.add_parser('age', help='Retrieves the age')
        age_parser.add_argument('--Name', type=str, default=False, help='Selects person')#this command starts the code to find the persons age

        dob_parser = subparsers.add_parser('DOB', help='retrieves the date of birth')
        dob_parser.add_argument('--Name', type=str, default=False, help='Selects person ')

        dod_parser = subparsers.add_parser('DOD', help='Retreives the date of death')
        dod_parser.add_argument('--Name', type=str, default=False, help='Selects person')

        load_parser = subparsers.add_parser('Load', help='Prints the data collected about the person')
        load_parser.add_argument('--Name', type=str, default=False, help='Selects person')

        setfname_parser = subparsers.add_parser('set_name', help='sets the variable for testing')
        setfname_parser.add_argument('--Name', type=str, default=False, help='sets the name to the input')

        setage_parser = subparsers.add_parser('set_age', help='sets the age for testing')
        setage_parser.add_argument('--age', type=str, default=False, help='sets the age to input')

        setdob_parser = subparsers.add_parser('set_dob', help='sets the dob for testing')
        setdob_parser.add_argument('--dob', type=str, default=False, help='sets the dob to input')

        setdod_parser = subparsers.add_parser('set_dod', help='sets the dod for testing')
        setdod_parser.add_argument('--dod', type=str, default=False, help='sets the dod to input')

        args = parser.parse_args()
        x = Person(args.Name)
        x.load()
        if args.command == 'name':
            name = x.get_fname()
            print(name)

        elif args.command == 'age':
            age = x.get_age()
            print(age)


        elif args.command == 'dob':
            dob = x.get_dob()
            print(dob)

        elif args.command == 'dod':
            dod = x.get_dod()
            print(dod)





        elif args.command == 'setfname':
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

    parser = argparse.ArgumentParser(description='Find data about someone')
    subparsers = parser.add_subparsers(help='commands', dest='command')
