import pytest
from porcupine.base import Serializer


class User(object):
    def __init__(self, name=None, surname=None, age=None):
        self.name = name
        self.surname = surname
        self.age = age


class Organisation(object):
    def __init__(self, user: User, name: str):
        self.user = user
        self.name = name


class UserSerializer(Serializer):
    name: str
    surname: str
    age: int = None


class OrganisationSerializer(Serializer):
    user: UserSerializer
    name: str


@pytest.fixture
def user():
    user = User('user_name', 'user_surname', 23)
    return user


@pytest.fixture
def organisation(user):
    organisation = Organisation(user, 'organisation_name')
    return organisation


class TestSimpleObject:
    def test_nested_serializer(self):
        user = User('user_name', 'user_surname', 23)
        organisation = Organisation(user, 'organisation_name')

        dictionary = OrganisationSerializer(organisation).dict()
        assert dictionary == {
            "user": {
                'name': 'user_name',
                'surname': 'user_surname',
                'age': 23
            },
            'name': 'organisation_name',
        }
