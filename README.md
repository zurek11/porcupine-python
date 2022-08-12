# porcupine-python

[![codecov](https://codecov.io/gh/zurek11/porcupine-python/branch/master/graph/badge.svg)](https://codecov.io/gh/zurek11/porcupine-python)

Hi. I am a small and lovely porcupine 🦔. I am here to serialize your objects 💪!

## Usage

**porcupine-python** is used for type and nested serialization of any objects with attributes into dictionaries.
It has a very good use, for example, in the **Django framework**. See [Django compatibility](#django-compatibility).

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

## Django compatibility

### Example model

```python
import uuid

from django.db import models
from django.utils.translation import gettext as _


class User(models.Model):
    class UserStatus(models.TextChoices):
        WAITING = 'waiting', _('Waiting')
        APPROVED = 'approved', _('Approved')
        BLOCKED = 'blocked', _('Blocked')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(null=False, unique=True, verbose_name=_('user_email'))
    nickname = models.CharField(max_length=100, null=False, unique=True, verbose_name=_('user_nickname'))
    name = models.CharField(null=True, max_length=30, verbose_name=_('user_name'))
    surname = models.CharField(null=True, max_length=150, verbose_name=_('user_surname'))
    amount = models.DecimalField(null=False, max_digits=10, decimal_places=2, default=0, verbose_name=_('user_amount'))
    status = models.CharField(
        max_length=15, null=False, choices=UserStatus.choices, default=UserStatus.WAITING, verbose_name=_('user_status')
    )
    is_active = models.BooleanField(null=False, default=True, verbose_name=_('user_is_active'))
    created_at = models.DateTimeField(auto_now_add=True)
```


### Example serializer

```python
from typing import Union
from uuid import UUID
from datetime import datetime
from decimal import Decimal

from porcupine.base import Serializer

from apps.core.models import User


class UserSerializer:
    class Base(Serializer):
        id: UUID
        email: str
        nickname: str
        name: str = None
        surname: str = None
        full_name: str = None
        amount: Decimal
        status: User.UserStatus
        is_active: bool
        created_at: datetime

        @staticmethod
        def resolve_full_name(data, **kwargs) -> Union[str, None]:
            # You can also use request in resolvers
            request = kwargs.get('request')

            if hasattr(data, 'name') and hasattr(data, 'surname'):
                full_name = f'{data.name} {data.surname}'
            else:
                full_name = None

            return full_name
```

### Example serializing

```python
from django.views import View
from django.http import JsonResponse

from apps.core.models import User
from apps.core.serializers.user import UserSerializer


class UserDetail(View):
    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise Some404Exception

        serialized_user = UserSerializer.Base(user, request=request).dict()

        # You can also make custom response with a serializer as an argument
        return JsonResponse(serialized_user)
```

---
Made with ❤ by Adam Žúrek & [BACKBONE s.r.o.](https://www.backbone.sk/en/)
