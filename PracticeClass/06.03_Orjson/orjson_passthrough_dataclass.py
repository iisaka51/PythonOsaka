import orjson, dataclasses

@dataclasses.dataclass
class User:
    id: str
    name: str
    password: str

def user_object(obj):
    if isinstance(obj, User):
        return {"id": obj.id, "name": obj.name}
    raise TypeError

data = orjson.dumps(User("3b1", "asd", "zxc"))
print('DATA:', repr(data))
print('NORMAL:', data)

try:
    data = orjson.dumps(User("3b1", "asd", "zxc"),
                        option=orjson.OPT_PASSTHROUGH_DATACLASS)
except TypeError as msg:
    print(' ERROR:', msg)

data = orjson.dumps(
        User("3b1", "asd", "zxc"),
        option=orjson.OPT_PASSTHROUGH_DATACLASS,
        default=user_object,
    )
print('CUSTOM:', data)
