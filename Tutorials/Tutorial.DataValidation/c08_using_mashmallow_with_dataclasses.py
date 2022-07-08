from marshmallow import Schema, fields, validate, ValidationError
from dataclasses import dataclass, asdict
from test_data import users

class UserSchema(Schema):
    id = fields.Integer(validate=validate.Range(min=1))
    username = fields.Str(validate=validate.Length(max=20))
    email = fields.Email()
    age = fields.Integer(validate=validate.Range(min=1))

_validator = UserSchema()
@dataclass
class User:
    id: int
    username: str
    email: str
    age: int

    def __post_init__(self):
        _validator.load(self.__dict__)


def parse_user(data):
    for user in users:
        try:
            user =  User( **user )
            print(f'OK: {user}')
        except ValidationError as e:
            print(f'NG: {user}')
            print(e)

# parse_user(users)
