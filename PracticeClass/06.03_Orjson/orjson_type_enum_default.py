import enum, orjson

class Custom:
    def __init__(self, val):
        self.val = val

def custom_obj(obj):
    if isinstance(obj, Custom):
        return obj.val
    raise TypeError

class CustomEnum(enum.Enum):
    ONE = Custom(1)

data = orjson.dumps(CustomEnum.ONE, default=custom_obj)
print(data)
