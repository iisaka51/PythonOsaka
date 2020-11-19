class Parent:
    val = 'parent class variable'
    def __init__(self):
        self.val = 'instance variable'

    def method(self):
        return 'instance method called', self.val

    @classmethod
    def classmethod(cls):
        return 'class method called', cls.val

    @staticmethod
    def staticmethod():
        return 'static method called', Parent.val

class Child(Parent):
    val = 'child class variable'
    pass

obj = Child()
print( obj.method() )
print( obj.classmethod() )
print( obj.staticmethod() )
