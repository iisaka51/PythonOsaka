from datetime import datetime, date
from pydantic import (
        BaseModel, ValidationError, validator, PositiveInt, EmailStr
    )
from pydantic.dataclasses import dataclass
from test_data import users

@dataclass
class User:
    id: int
    username: str
    birthday: date
    email: EmailStr
    age: PositiveInt


birthday_list = [
  { 'birthday': '1994-07-21' },
  { 'birthday': '1962-01-13' },
  { 'birthday': '1970-17-22' },
]

def parse_user(data):
    for num, user in enumerate(users):
        try:
            # user |= birthday_list[num]       # for Python 3.9 or later
            user.update(birthday_list[num])
            user =  User( **user )
            print(f'OK: {user}')
        except ValidationError as e:
            print(f'NG: {user}')
            print(e)

# parse_user(users)
