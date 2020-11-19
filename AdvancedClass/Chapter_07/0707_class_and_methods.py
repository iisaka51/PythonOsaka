class Artist:
    def __init__(self, firstname='', lastname=''):
        if type(firstname) != str or type(lastname) != str:
            raise(ValueError("firstname and lastname must be 'str'"))
        self.firstname = firstname
        self.lastname = lastname

    def show_name(self):
        return( f'{self.firstname}_{self.lastname}')

queen = Artist('Freddie', 'Mercury')
print(queen.show_name())
