class User(object):
    def __init__(self,
        id: int = 0,
        name: str = '',
        email: str = '',
    ):
        self.__id = id
        self.__name = name
        self.__email = email

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def email(self):
        return self.__email

    def __repr__(self):
        v = (  'User('
              f'id={self.__id}, '
              f'name="{self.__name}", '
              f'email="{self.__email})"' )
        return v

user = User(id=1, name='Freddie', email='freddie@example.com')

# user
# user.name
# user.name = 'Brian'
