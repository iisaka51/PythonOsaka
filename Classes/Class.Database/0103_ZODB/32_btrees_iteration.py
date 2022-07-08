from BTrees.OOBTree import OOBTree

t = OOBTree()
t.update({1: "red", 2: "green", 3: "blue", 4: "spades"})

v1 = t.keys()
v2 = t
v3 = t.iteritems()

def func1():
    for k in t.keys():
        print(f'{k} ', end='')

def func2():
    for k in t:
        print(f'{k} ', end='')

def func3():
    for k in t.iteritems():
        print(f'{k} ', end='')

# print(v1)
# print(v2)
# print(v3)
# func1()
# func2()
# func3()
