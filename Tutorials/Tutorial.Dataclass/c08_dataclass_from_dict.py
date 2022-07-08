from dataclasses import dataclass

user_data = {
    'id': 1,
    'name': 'Freddie',
    'email': 'freddie@example.com'
}

@dataclass
class User(object):
    id: int = 0
    name: str = ''
    email: str = ''

user = User(**user_data)
