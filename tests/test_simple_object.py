import pytest
from pydantic import ValidationError
from simple_serializer.base import Serializer


class User(object):
    def __init__(self, name=None, surname=None, age=None):
        self.name = name
        self.surname = surname
        self.age = age


class UserSerializer(Serializer):
    name: str
    surname: str
    age: int = None


@pytest.fixture
def user_full():
    user = User('foo', 'bar', 23)
    return user


@pytest.fixture
def user_required_only():
    user = User('foo', 'bar')
    return user


@pytest.fixture
def user_none():
    user = User()
    return user


class TestSimpleObject:
    def test_successful_serialisation(self, user_full):
        dictionary = UserSerializer(user_full).dict()
        assert dictionary == {'name': 'foo', 'surname': 'bar', 'age': 23}

    def test_non_required_attributes(self, user_required_only):
        dictionary = UserSerializer(user_required_only).dict()
        assert dictionary == {'name': 'foo', 'surname': 'bar', 'age': None}

    def test_required_attributes(self, user_none):
        expected_errors = [
            {'loc': ('name',), 'msg': 'none is not an allowed value', 'type': 'type_error.none.not_allowed'},
            {'loc': ('surname',), 'msg': 'none is not an allowed value', 'type': 'type_error.none.not_allowed'}
        ]

        with pytest.raises(ValidationError) as exception:
            UserSerializer(user_none).dict()
        assert exception.value.errors() == expected_errors
