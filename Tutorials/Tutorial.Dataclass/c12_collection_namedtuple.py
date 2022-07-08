from collections import namedtuple

User = namedtuple("User", "id name email")

user = User(1, "Freddie", "freddie@example.com")

# user
# user[1]
# user.name
# user.name = "Brian"

