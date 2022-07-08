class Person():
    def __init__(self, name_str):
        print('init name')
        self.__hidden_name = name_str

    def get_name(self):
        print('get_name called')
        return self.__hidden_name

    def set_name(self, name_str):
        print(f'set_name called with {name_str}')
        self.__hidden_name = name_str

    name = property(get_name, set_name)

p = Person('Freddie')
print(p.name)

p.set_name('David')
p.name = 'Eddie'

print(dir(p))
