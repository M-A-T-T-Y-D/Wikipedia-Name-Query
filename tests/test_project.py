import pytest

from wikipedia_name_query.Person import Person

class Tests():
    
    def test_name():
        x = Person("Donald Trump")
        assert x.name == "Donald Trump"
        
        assert x.fullname == "Donald Trump Jr"


    #def test_dob():
        
        #assert self.dob == "1946-06-14"

    #def test_dod():

        #assert self.dod == "Still Alive"
    
    #def test_age():

        #assert self.age == "77"