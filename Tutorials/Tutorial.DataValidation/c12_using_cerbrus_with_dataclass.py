from cerberus import Validator, DocumentError
from datetime import datetime
from dataclasses import dataclass
from pydantic import (
        BaseModel, ValidationError, validator, PositiveInt, EmailStr
    )

class ValidateError(BaseException):
    pass

to_date = lambda s: datetime.strptime(s, '%Y-%m-%d')
schema_user = {
    'id': {'type': 'integer', 'min': 1 },
    'username': {
        'type': 'string',
        'minlength': 8, 'maxlength': 20 },
    'email': {
        'type': 'string',
        'regex': "^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$" },
    'birthday': {'type': 'date', 'coerce': to_date },
    'age': {'type': 'integer', 'min': 0},
    }

@dataclass
class User:
    id: int
    username: str
    birthday: str
    email: str
    age: int

    def __post_init__(self):
        if not v.validate(self.__dict__):
            raise ValidateError(v.errors)

class UserValidator(Validator):
    def validate_user(self, obj):
        return self.validate(obj.__dict__)

v = UserValidator(schema_user)


users = [
     User( id=1, username="Jack Johnson",
               email="jackJohnson@gmail.com",
               birthday='1970-07-20', age=52  ),
     User( id=2, username="Goichi Iisaka",
               email="jackJohnson@gmail.com",
               birthday='1962-01-13', age=60 ),
]

users[1].email = "jackJohnson@gmail."
users[1].age = -20

for user in users:
    if v.validate_user(user):
        print(user)
    else:
        print('invalid data')
        print(v.errors)
