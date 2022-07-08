from datetime import datetime
from pydantic import (
        BaseModel, ValidationError, validator, PositiveInt, EmailStr
    )
from test_data import users

class User(BaseModel):
    id: int
    username: str
    birthday: str
    email: EmailStr
    age: PositiveInt

    @validator('birthday')
    def valid_date(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("date must be in YYYY-MM-DD format.")


birthday_list = [
  { 'birthday': '1994-07-21' },
  { 'birthday': '1962-01-13' },
  { 'birthday': '1970-07-22' },
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
