from dataclasses import dataclass

@dataclass
class User(object):
    id: int = 0
    name: str = ''
    email: str = ''

user = User(id=1, name='Freddie', email='freddie@example.com')

# user
# user.name
