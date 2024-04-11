import pytest
from wikipedia_name_query.Query import Query




#class q_test():
@pytest.fixture
def query_test():
    Querytest = Query()
    output = Querytest.get_person_info("Donald Knuth")
    return output
def test_full_name(query_test):
    assert query_test[0][0] == "Donald Knuth"
    assert query_test[0][1] == "1938-01-10"
    assert query_test[0][2] is None
    
def test_rndm():
    Querytest = Query()
    output = Querytest.get_person_info("google")
    assert output is None

def test_None():
    Querytest = Query()
    with pytest.raises(ValueError) as excinfo:
        Querytest.get_person_info(None)
    
    