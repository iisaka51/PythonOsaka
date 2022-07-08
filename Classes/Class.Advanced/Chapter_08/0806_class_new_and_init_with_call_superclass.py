class Person(object):
    def __new__(cls):
        print('new is called')
        return super().__new__(cls)

    def __init__(self):
        print('init is called')
        super().__init__()

obj = Person()
