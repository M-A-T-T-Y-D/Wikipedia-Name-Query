import pytest

from wikipedia_name_query.Person import Person


class Tests():
    @pytest.fixture
    def person(self):
        x = Person("Donald Knuth")
        x.load()
        return x

    def test_name(self, person):
        assert person.name == "Donald Knuth"
        assert person.fullname == "Donald Knuth"

    def test_dob(self, person):
        assert person.dob == "1938-01-10"

    def test_dod(self, person):
        assert person.dod is None

    def test_age(self, person):
        assert person.age == 86
