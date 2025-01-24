"""
Imported Modules:
- logging: Allows for logging messages to the console or a file
- SPARQLWrapper: A Python library for querying SPARQL endpoints
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

class Query():
    '''
    This is a class used to hold the query
    '''
    @staticmethod
    def get_person_info(person_name):
        '''
        This function queries dbpedia for the entered person and retrieves the data needed,
        this is then put into a format and ready to be output
        
        Parameters
        -----------
        person_name : str
            The name of the person to query
        '''
        # Check if the person_name is None
        if person_name is None:
            logger.error("person_name is None")
            raise ValueError("person_name cannot be None")

        # Set up the SPARQL endpoint
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery("""
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX dbo: <http://dbpedia.org/ontology/>

            SELECT ?name ?birthDate ?deathDate
            WHERE {
                ?person foaf:name ?name ;
                        dbo:birthDate ?birthDate .
                OPTIONAL { ?person dbo:deathDate ?deathDate }
                FILTER (lang(?name) = 'en')
                FILTER (regex(?name, "%s", "i"))
            }
        """ % person_name)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        # Log the input name and results
        #logger.debug("Querying for person: %s", person_name)
        #logger.debug("Query results: %s", results)

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
