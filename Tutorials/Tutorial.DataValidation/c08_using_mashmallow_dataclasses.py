from marshmallow import Schema, validate, ValidationError
from marshmallow import fields as mfields
from marshmallow_dataclass import dataclass, class_schema
from dataclasses import field, asdict
from marshmallow import Schema
from typing import ClassVar, Type
from test_data import users

@dataclass
class User:
    id: int = field(metadata = { "validate": validate.Range(min=1) })
    username: str  = field(metadata = { "validate":  validate.Length(max=20) })
    email: str  = field(metadata = { "validate":  validate.Email() })
    age: int  = field(metadata = { "validate": validate.Range(min=1) })
    Schema: ClassVar[Type[Schema]] = Schema

def parse_user(data):
    for user in users:
        user =  User( **user )
        try:
            class_schema(User)().load(asdict(user))
            print(f'OK: {user}')
        except ValidationError as e:
            print(f'NG: {user}')
            print(e)

# parse_user(users)
