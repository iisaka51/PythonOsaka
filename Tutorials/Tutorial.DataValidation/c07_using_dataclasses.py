import re
from dataclasses import dataclass
from test_data import users

@dataclass
class User:

    id: str
    username: str
    email: str
    age: int


def parse_user(data):
    for user in users:
        user =  User( **user )
        print(user)

# parse_user(users)
