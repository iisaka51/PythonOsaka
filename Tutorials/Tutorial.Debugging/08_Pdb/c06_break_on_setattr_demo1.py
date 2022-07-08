from pdb import break_on_setattr

@break_on_setattr('bar')
class Foo(object):
    pass

f = Foo()
f.bar = 42
