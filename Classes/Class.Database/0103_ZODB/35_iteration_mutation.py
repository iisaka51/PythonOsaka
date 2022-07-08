from BTrees.IIBTree import *
s = IISet(range(10))
v1 = list(s)

def func1():
    for i in s:
        print(f'{i} ', end='')
        s.remove(i)

v2 = list(s)

# print(v1)
# func1()
# print(v2)
