class Person():
    def __init__(self, name_str=''):
        print('init name')
        self.__hidden_name = name_str

    @property
    def name(self):
        print('get name called')
        return self.__hidden_name

    @name.setter
    def name(self, name_str=''):
        print(f'set name called with {name_str}')
        self.__hidden_name = name_str

p = Person('Freddie')
print(p.name)

p.name = 'Eddie'
print(p.name)

