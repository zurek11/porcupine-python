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
        allow_full_name = kwargs.get('allow_full_name', False)
        fullname = None

        if allow_full_name:
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


class TestCustomArguments:
    def test_custom_argument_true(self, user):
        dictionary = UserSerializer(user, allow_full_name=True).dict()
        assert dictionary == {'name': 'foo', 'surname': 'bar', 'full_name': 'foo bar'}

    def test_custom_argument_false(self, user):
        dictionary = UserSerializer(user, allow_full_name=False).dict()
        assert dictionary == {'name': 'foo', 'surname': 'bar', 'full_name': None}
