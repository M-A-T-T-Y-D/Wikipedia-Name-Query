'''
The module SPARQLWrapper is used to send and format the sql query 
'''

from SPARQLWrapper import SPARQLWrapper, JSON



class Query():
    '''
    This is a class used to hold the query
    '''
    @staticmethod
    def get_person_info(person_name):
        '''
        This function querys dhpedia for the emtered person and retreives the data needed,
        this is then put into a format and ready to be output
        '''
        # Set up the SPARQL endpoint
        if person_name is None:
            raise ValueError
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
        print(person_name, results)
        for result in results["results"]["bindings"]:
            full_name = result["name"]["value"]
            birth_date = result["birthDate"]["value"]
            death_date = result["deathDate"]["value"] if "deathDate" in result else None
            person_info.append([full_name, birth_date, death_date])
        if person_info == []:
            return None
        return person_info
