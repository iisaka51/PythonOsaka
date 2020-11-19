class SampleMeta(type):
    def __new__(cls, clsname, superclasses, attributedict):
        x = super().__new__(cls, clsname, superclasses, attributedict)
        x.name = 'Python'
        return x

class Parent:
    pass


class Child(Parent, metaclass=SampleMeta):
    pass

print(Child.name)
