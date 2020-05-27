# porcupine-python

[![codecov](https://codecov.io/gh/zurek11/porcupine-python/branch/master/graph/badge.svg)](https://codecov.io/gh/zurek11/porcupine-python)

Hi. I am a fucking porcupine 🦔. I am here to serialize your responses 💪. 

## Usage

porcupine-python is used for type and nested serialization of any objects with attributes into dictionaries.

### Simple usage

First we need to create some simple class:

```python
class User(object):
    def __init__(self, name=None, surname=None, age=None):
        self.name = name
        self.surname = surname
        self.age = age
```

Second we create serializer for this type of class:

```python
from porcupine.base import Serializer

class UserSerializer(Serializer):
    name: str
    surname: str
    age: int = None
```

Final usage with different created instances looks like this:

```python
# User instance with all attributes
user = User('foo', 'bar', 23)

dictionary = UserSerializer(user).dict()
# dictionary: {'name': 'foo', 'surname': 'bar', 'age': 23}

# User instance with only required attributes
user = User('foo', 'bar')

dictionary = UserSerializer(user).dict()
# dictionary: {'name': 'foo', 'surname': 'bar', 'age': None}

# User instance with all None attributes
user = User()

dictionary = UserSerializer(user).dict()
# raised ValidationError
```

### Usage of resolvers

First we need to create some class which instances will be resolved:

```python
class User(object):
    def __init__(self, name=None, surname=None, age=None):
        self.name = name
        self.surname = surname
```

Serializer for that class:

```python
from porcupine.base import Serializer

class UserSerializer(Serializer):
    name: str = None
    surname: str = None
    full_name: str = None

    @staticmethod
    def resolve_full_name(data):
        fullname = None

        if data.name and data.surname:
            fullname = f'{data.name} {data.surname}'
        elif data.name:
            fullname = data.name
        elif data.surname:
            fullname = data.surname

        return fullname
```

Serialized user instance:

```python
user = User('foo', 'bar')

dictionary = UserSerializer(user).dict()
# dictionary: {'name': 'foo', 'surname': 'bar', 'full_name': 'foo bar'}
```

---
Made with ❤ by Adam Žúrek & [BACKBONE s.r.o.](https://www.backbone.sk/en/)
