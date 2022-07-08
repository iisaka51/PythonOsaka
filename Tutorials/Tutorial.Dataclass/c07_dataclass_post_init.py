from dataclasses import dataclass, InitVar

@dataclass
class User(object):
    id: InitVar[int] = 0
    name: str = ''
    email: str = ''

    def __post_init__(self, id):
        if id < 0:
            raise(ValueError('ID must be positive integer'))

user = User(id=-1, name='Freddie', email='freddie@example.com')
