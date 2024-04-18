import pytest
from wikipedia_name_query.Query import Query




#class q_test():
@pytest.fixture
def query_test1():
    query_test = Query()
    output = query_test.get_person_info("Donald Knuth")
    return output
def test_full_name(query_test1):
    assert query_test1[0][0] == "Donald Knuth"
    assert query_test1[0][1] == "1938-01-10"
    assert query_test1[0][2] is None

def test_rndm():
    query_test = Query()
    output = query_test.get_person_info("google")
    assert output is None

def test_none():
    query_test = Query()
    with pytest.raises(ValueError):
        query_test.get_person_info(None)
