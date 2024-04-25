from wikipedia_name_query.person import Person
import pytest



class Tests():
    """
    Class to hold tests
    """
    @pytest.fixture
    def person(self):
        """
        This function loads the data to be used it only needs to be opened once
        """
        x = Person("Donald Knuth")
        x.load()
        return x

    def test_name(self, person):
        """
        Checks if the name returned is correct
        """
        assert person.name == "Donald Knuth"
        assert person.fullname == "Donald Knuth"

    def test_dob(self, person):
        """
        Checks to see wether the date of birth is correct
        """
        assert person.dob == "1938-01-10"

    def test_dod(self, person):
        """
        Tests wether the person is dead
        """
        assert person.dod is None

    def test_age(self, person):
        """
        tests wether the age is calculated correctly
        """
        assert person.age == 86
