import re
from dataclasses import dataclass
from test_data import users

@dataclass
class User:

    id: str
    username: str
    email: str
    age: int

    def __post_init__(self):
        if not isinstance(self.age, int):
            raise TypeError(f'Age must be "int"')
        if self.age < 0:
            raise ValueError("Age must be postive value.")
        regex = "^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$"
        if not isinstance(self.email, str):
            raise TypeError(f'Email must be "str"')
        if not re.match(regex, self.email):
            raise ValueError("Invalid email address.")
        if not isinstance(self.username, str):
            raise TypeError(f'Username must be "str"')
        if len(self.username) > 20:
            raise ValueError("Username must be less than 20 characters.")


def parse_user(data):
    for user in users:
        user =  User( **user )
        print(user)

# parse_user(users)
