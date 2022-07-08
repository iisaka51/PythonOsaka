import re
from dataclasses import dataclass
from test_data import users

@dataclass
class User:

    id: str
    username: str
    email: str
    age: int

    def __init__(self, id, username, email, age, enable=True):
        self.id = id
        self.username = username
        self.email = email
        self.age = age
        self.enable = enable    # フィールドとして扱われない


def parse_user(data):
    for user in users:
        user =  User( **user )
        print(user)

# parse_user(users)
