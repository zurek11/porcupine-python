from typing import List
from pydantic import BaseModel


class Serializer(BaseModel):
    def __init__(self, data: object, **kwargs):
        init_input = {}

        for key, value in self.__fields__.items():
            resolver = f"resolve_{key}"
            if hasattr(self, resolver):
                if kwargs:
                    init_input[key] = getattr(self, resolver)(data, **kwargs)
                else:
                    init_input[key] = getattr(self, resolver)(data)
            elif issubclass(value.type_, Serializer) and getattr(data, key) is not None:
                if value.sub_fields is not None and isinstance(value.sub_fields, List):
                    if len(value.sub_fields) > 1:
                        RuntimeError('Only one type must be specified.')
                    elif issubclass(value.sub_fields[0].type_, Serializer):
                        result = []
                        for item in getattr(data, key).all():
                            result.append(value.sub_fields[0].type_(data=item, **kwargs))
                        init_input[key] = result
                else:
                    init_input[key] = value.type_(data=getattr(data, key), **kwargs)
            elif hasattr(data, key):
                init_input[key] = getattr(data, key)

        super().__init__(**init_input)
