from collections import namedtuple

User = namedtuple("User", "id name email")

def get_user(*args):
    # ...
    id = 1
    name = "Freddie"
    email = "freddie@exampl.com"

    return id, name, email

v1 = get_user()
