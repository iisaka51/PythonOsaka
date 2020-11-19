class Artist1():
    def __init__(self, firstname='', lastname=''):
        self.firstname = firstname
        self.lastname = lastname

class Artist2():
    def __init__(self, firstname='', lastname=''):
        self.__firstname = firstname
        self.__lastname = lastname

queen = Artist1('Freddie', 'Mercury')
print(f'\n{queen.__class__}:', dir(queen))
print("Queen's main vocal is ", queen.firstname )

whitesnake = Artist2('David','Coverdale')
print(f'\n{whitesnake.__class__}:', dir(whitesnake))
print("Whitesnake's main vocal is ", whitesnake.__firstname )

