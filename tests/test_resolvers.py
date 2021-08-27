from porcupine.base import Serializer


class User(object):
    def __init__(self, name=None, surname=None, age=None):
        self.name = name
        self.surname = surname
        self.age = age


class UserSerializer(Serializer):
    name: str
    surname: str
    age: int = None

    @staticmethod
    def resolve_surname(data: User):
        return "Dent"


class TestResolver:
    def test_nested_serializer(self):
        user = User('Aurthur', 'NotDent', 23)

        dictionary = UserSerializer(user).dict()
        assert dictionary == {
            'name': 'Aurthur',
            'surname': 'Dent',
            'age': 23
        }
