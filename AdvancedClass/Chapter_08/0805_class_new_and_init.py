class Person:
    def __new__(cls):
        print('new is called')

    def __init__(self):
        print('init is called')

obj = Person()
