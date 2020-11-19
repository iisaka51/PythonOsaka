class Artist():
    def __init__(self):
        self.firstname = ''
        self.lastname = ''

    def show_name(self):
        return( f'{self.firstname}_{self.lastname}')


queen = Artist()
queen.firstname = 'Freddie'
queen.lastname = 'Mercury'

print(queen.show_name())

