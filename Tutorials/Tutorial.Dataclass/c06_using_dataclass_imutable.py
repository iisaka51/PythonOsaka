from dataclasses import dataclass

@dataclass(frozen=True)
class User(object):
    id: int = 0
    name: str = ''
    email: str = ''

user = User(id=1, name='Freddie', email='freddie@example.com')

# user
# user.name
