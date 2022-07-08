from collections import namedtuple

User = namedtuple("User", "id name email",
                  defaults=[1, "", ""] )

# User = namedtuple("User", "id name email")
# User.__new__.__defaults__ = (1, "", "")

user = User(name="Freddie", email="freddie@example.com")

# user
