from SPARQLWrapper import SPARQLWrapper, JSON




class Query():
    @staticmethod
    def get_person_info(person_name):
        # Set up the SPARQL endpoint
        if person_name == None:
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
            #print(person_info)
        if person_info == []:
            return None
        return person_info
    
    
        



