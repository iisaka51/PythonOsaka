from pdb import break_on_setattr

class Foo(object):
    pass
a = Foo()
b = Foo()

def break_if_a(obj, value):
    return obj is a

break_on_setattr('bar', condition=break_if_a)(Foo)
b.bar = 10   # ブレークはしない
a.bar = 42   # ここでブレーク
