"""Entry point for wikipedia_name_query."""
from wikipedia_name_query.Commands import Commands

def main():
    cli = Commands()
    cli.commands()


if __name__ == "__main__":
    main()
