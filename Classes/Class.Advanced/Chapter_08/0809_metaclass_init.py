# オブジェクトの初期化
class MyClass:
    def __init__(self):
        self.name = 'Python'

a = MyClass()
b = MyClass()

print(a.name, b.name)

# クラスの初期化
class MyMeta:
    def __init__(cls, clsname, superclasses, attributedict):
        cls.name = 'Python'

class XClass(metaclass=MyMeta):
    pass

class YClass(metaclass=MyMeta):
    pass

print(XClass.name, YClass.name)
