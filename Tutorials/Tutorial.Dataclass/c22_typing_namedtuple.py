from typing import NamedTuple

class User(NamedTuple):
    id: int
    name: str
    email: str

def get_user(*args) -> User:
    # ...
    id = 1
    name = "Freddie"
    email = "freddie@exampl.com"

    return User(id, name, email)

v1 = get_user()
