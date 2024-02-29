from SPARQLWrapper import SPARQLWrapper, JSON
from datetime import datetime


class Query():
    def get_person_info(person_name):
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
        person_info = []

        for result in results["results"]["bindings"]:
            full_name = result["name"]["value"]
            birth_date = result["birthDate"]["value"]
            death_date = result["deathDate"]["value"] if "deathDate" in result else "Still alive"
            person_info.append((full_name, birth_date, death_date))
        return person_info
        



    def calculate_age(birth_date, death_date=None):
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
        if death_date:
            death_date = datetime.strptime(death_date, "%Y-%m-%d")
            age = (death_date - birth_date).days // 365
        else:
            age = (datetime.now() - birth_date).days // 365
        return age