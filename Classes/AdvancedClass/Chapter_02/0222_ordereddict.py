from collections import OrderedDict

d = {'b': 1, 'a': 2, 'c':3}
k,v=d.popitem()
print(type(d))
print(k,v)
print(d.items())

od = OrderedDict([('b', 1), ('a', 2), ('c',3)])
k,v=od.popitem(last=False)
print(type(od))
print(k,v)
print(od.items())

od = OrderedDict([('b', 1), ('a', 2), ('c',3)])
k,v=od.popitem(last=True)
print(type(od))
print(k,v)
print(od.items())
