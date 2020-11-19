class Artist():
    def __init__(self, firstname='', lastname=''):
        self.firstname = firstname
        self.lastname = lastname

    def __repr__(self):
        return( f'repr {self.firstname}_{self.lastname}')

    def __str__(self):
        return( f'str {self.firstname}_{self.lastname}')

    def show_name(self):
        return( f'{self.firstname}_{self.lastname}')


queen = Artist('Freddie', 'Mercury')

print(queen.show_name())
print(queen)
print(str(queen))
print(repr(queen))
