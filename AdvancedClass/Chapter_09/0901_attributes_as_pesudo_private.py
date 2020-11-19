class Person():
    def __init__(self, name):
        print('init name')
        self.__name = name

    def get_name(self):
        print('get name')
        return self.__name

    def set_name(self, name):
        print('set name')
        self.__name = name

p = Person('Freddie')
print(p.get_name())
print(p.__name)
