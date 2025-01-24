"""
Imported Modules:
- logging: Allows for logging messages to the console or a file.
- SPARQLWrapper: A Python library for querying SPARQL endpoints.
"""
import logging
from SPARQLWrapper import SPARQLWrapper, JSON

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('app.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
file_handler.flush()
logger.addHandler(file_handler)


class Query:
    '''
    A class for executing SPARQL queries to retrieve information about a person.

    Methods
    -------
    get_person_info(person_name: str) -> list[list[str | None]] | None
        Queries DBpedia for the given person and retrieves relevant data, such as their
        name, birth date, and (optionally) death date.
    '''

    @staticmethod
    def get_person_info(person_name: str) -> list[list[str | None]] | None:
        '''
        Queries DBpedia for the given person and retrieves relevant data, 
        such as their name, birth date, and (optionally) death date.
        
        Parameters
        ----------
        person_name : str
            The name of the person to query.

        Returns
        -------
        person_info : list of lists or None
            A list of lists where each inner list contains the full name (str),
            birth date (str), and optionally the death date (str or None). 
            Returns None if no information is found.

        Raises
        ------
        ValueError
            If the `person_name` parameter is None.
        '''
        if person_name is None:
            logger.error("person_name is None")
            raise ValueError("person_name cannot be None")

        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery(f"""
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX dbo: <http://dbpedia.org/ontology/>

            SELECT ?name ?birthDate ?deathDate
            WHERE {{
                ?person foaf:name ?name ;
                        dbo:birthDate ?birthDate .
                OPTIONAL {{ ?person dbo:deathDate ?deathDate }}
                FILTER (lang(?name) = 'en')
                FILTER (regex(?name, "{person_name}", "i"))
            }}
        """)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        logger.debug("Querying for person: %s", person_name)
        logger.debug("Query results: %s", results)

        person_info = []
        for result in results["results"]["bindings"]:
            full_name = result["name"]["value"]
            birth_date = result["birthDate"]["value"]
            death_date = result["deathDate"]["value"] if "deathDate" in result else None
            person_info.append([full_name, birth_date, death_date])

        if not person_info:
            logger.info("No information found for person: %s", person_name)
            return None

        logger.info("Retrieved information for person: %s", person_name)
        return person_info
