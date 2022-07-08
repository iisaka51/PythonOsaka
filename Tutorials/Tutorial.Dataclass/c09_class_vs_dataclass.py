from dataclasses import dataclass

class User_C(object):
    def __init__(self,
        id: int = 0,
        name: str = '',
        email: str = '',
    ):
        self.id = id
        self.name = name
        self.email = email

    def __repr__(self):
        v = (  'User('
              f'id={self.id}, '
              f'name="{self.name}", '
              f'email="{self.email})"' )
        return v


@dataclass
class User_D(object):
    id: int = 0
    name: str = ''
    email: str = ''

v1 = User_C(id=1, name='Freddie', email='freddie@example.com')
v2 = User_C(id=1, name='Freddie', email='freddie@example.com')

v3 = User_D(id=1, name='Freddie', email='freddie@example.com')
v4 = User_D(id=1, name='Freddie', email='freddie@example.com')

assert (v1 == v2) == False
assert (v3 == v4) == True

# v1, v3
