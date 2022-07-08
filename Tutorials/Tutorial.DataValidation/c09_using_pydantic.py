from pydantic import (
        BaseModel, ValidationError, validator, PositiveInt, EmailStr
    )
from test_data import users

class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    age: PositiveInt


def parse_user(data):
    for user in users:
        try:
            user =  User( **user )
            print(f'OK: {user}')
        except ValidationError as e:
            print(f'NG: {user}')
            print(e)

# parse_user(users)
