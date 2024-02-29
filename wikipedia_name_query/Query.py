from SPARQLWrapper import SPARQLWrapper, JSON
from datetime import datetime

def get_person_info(person_name):
        """
        This function holds the query used to collect data from wikipedia, it returns variables to
        Person file so they can be output.

        Parameters
        -----------
        results : str
            This is a string containing all the relevant information, it gets formatted and converted
            to a list
        person_info : List
            This is used to store the data in a searchable list

        Returns
        --------
        person_info
            The list is sent back to Person.py to be used to store all output data that is needed.
            If no person is found on wikipedia then it will return data for someone with a simmilar
            name
        """

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

        person_info = []

        for result in results["results"]["bindings"]:
            full_name = result["name"]["value"]
            birth_date = result["birthDate"]["value"]
            death_date = result["deathDate"]["value"] if "deathDate" in result else "Still alive"
            person_info.append((full_name, birth_date, death_date))
        return person_info
        
def calculate_age(birth_date, death_date=None):
        """
        The purpous of this function is to calculate the age of the person who had data queried of wikipedia

        Parameters
        -----------
        Birth_date : str
            The birth date in format from what was collected by the query
        Death_date : str
            The death date in format from what was collected from the query 
            (only needed if person isdead otherwise this is skipped)
        age : int
            The calculated age of the person
        Returns
        --------
        age
            The int is sent to Person.py to be output there when needed.
        """
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
        if death_date:
            death_date = datetime.strptime(death_date, "%Y-%m-%d")
            age = (death_date - birth_date).days // 365
        else:
            age = (datetime.now() - birth_date).days // 365
        return age