import pytest
from porcupine.base import Serializer


class User(object):
    def __init__(self, name=None, surname=None):
        self.name = name
        self.surname = surname


class UserSerializer(Serializer):
    name: str = None
    surname: str = None
    full_name: str = None

    @staticmethod
    def resolve_full_name(data, **kwargs):
        fullname = None

        if data.name and data.surname:
            fullname = f'{data.name} {data.surname}'
        elif data.name:
            fullname = data.name
        elif data.surname:
            fullname = data.surname

        return fullname


@pytest.fixture
def user():
    user = User('foo', 'bar')
    return user


@pytest.fixture
def user_none():
    user = User()
    return user


class TestSimpleObject:
    def test_resolved_full_name(self, user):
        dictionary = UserSerializer(user).dict()
        assert dictionary == {'name': 'foo', 'surname': 'bar', 'full_name': 'foo bar'}

    def test_successful_resolved_none(self, user_none):
        dictionary = UserSerializer(user_none).dict()
        assert dictionary == {'name': None, 'surname': None, 'full_name': None}
