import pytest
from wikipedia_name_query.query import Query




#class q_test():
@pytest.fixture
def query_test12():
    """
    This loads the data needed for tests
    """
    query_test = Query()
    output = query_test.get_person_info("Donald Knuth")
    return output
def test_full_name(query_test1):
    """
    Tests wether correct information is returned when full name is given
    """
    assert query_test1[0][0] == "Donald Knuth"
    assert query_test1[0][1] == "1938-01-10"
    assert query_test1[0][2] is None

def test_rndm():
    """
    Tests to see wether code will refuse to locate random inputs
    """
    query_test = Query()
    output = query_test.get_person_info("google")
    assert output is None

def test_none():
    """
    Tests to see if code will raise an error when nothing is entered
    """
    query_test = Query()
    with pytest.raises(ValueError):
        query_test.get_person_info(None)
