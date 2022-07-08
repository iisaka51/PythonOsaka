class User(object):
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

user = User(id=1, name='Freddie', email='freddie@example.com')

# user
# user.name
