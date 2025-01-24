import argparse
from wikipedia_name_query.person import Person


class Commands:
    """
    A class to define custom terminal commands for retrieving or modifying 
    information about a person.
    """

    def commands(self) -> None:
        """
        Configures terminal commands and provides information about them
        when using the `-h` or `--help` flags.

        Available Commands
        ------------------
        name : Retrieves the name of the person.
        age : Retrieves the age of the person.
        DOB : Retrieves the date of birth of the person.
        DOD : Retrieves the date of death of the person.
        Load : Loads and prints all data collected about the person.
        setfname : Sets a new full name for the person.
        setage : Sets a new age for the person.
        setdob : Sets a new date of birth for the person.
        setdod : Sets a new date of death for the person.
        """
        parser = argparse.ArgumentParser(description="Find data about someone")
        subparsers = parser.add_subparsers(help="commands", dest="command")

        name_parser = subparsers.add_parser("name", help="Retrieves the person's name")
        name_parser.add_argument("--Name", type=str, required=True, help="Selects person")

        age_parser = subparsers.add_parser("age", help="Retrieves the person's age")
        age_parser.add_argument("--Name", type=str, required=True, help="Selects person")

        dob_parser = subparsers.add_parser("DOB", help="Retrieves the person's date of birth")
        dob_parser.add_argument("--Name", type=str, required=True, help="Selects person")

        dod_parser = subparsers.add_parser("DOD", help="Retrieves the person's date of death")
        dod_parser.add_argument("--Name", type=str, required=True, help="Selects person")

        load_parser = subparsers.add_parser("Load", help="Prints all data collected about the person")
        load_parser.add_argument("--Name", type=str, required=True, help="Selects person")

        args = parser.parse_args()
        person = Person(args.Name)
        person.load()

        if args.command == "name":
            print(person.get_fname())

        elif args.command == "age":
            print(person.get_age())

        elif args.command == "DOB":
            print(person.get_dob())

        elif args.command == "DOD":
            print(person.get_dod())

        elif args.command == "setfname":
            fullname = person.set_fullname()
            print("You set the name to:", fullname)

        elif args.command == "setage":
            age = person.set_age()
            print("You set the age to:", age)

        elif args.command == "setdob":
            dob = person.set_dob()
            print("You set the date of birth to:", dob)

        elif args.command == "setdod":
            dod = person.set_dod()
            print("You set the date of death to:", dod)

        else:
            print("No such command. Please try again.")

