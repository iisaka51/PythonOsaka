from BTrees.IIBTree import *
s = IISet(range(10))

def func1():
    for i in list(s.keys()):
        print(f'{i} ', end='')
        s.remove(i)

# s
# s.keys()
# func1()
# s.keys()
# s
