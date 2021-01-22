import dataclasses, orjson, typing

@dataclasses.dataclass
class Member:
    id: int
    active: bool = dataclasses.field(default=False)

@dataclasses.dataclass
class Object:
    id: int
    name: str
    members: typing.List[Member]

data = orjson.dumps(Object(1, "a", [Member(1, True), Member(2)]))
print('  DATA:', repr(data))
print('NORMAL:', data)
