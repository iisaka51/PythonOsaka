class SampleMeta(type):
    def __new__(cls, clsname, superclasses, attributedict):
        print("clsname: ", clsname)
        print("superclasses: ", superclasses)
        print("attributedict: ", attributedict)
        return type.__new__(cls, clsname, superclasses, attributedict)

class Parent:
    pass


class Child(Parent, metaclass=SampleMeta):
    pass

# obj = Child()
