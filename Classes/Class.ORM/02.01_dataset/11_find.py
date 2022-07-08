from testdb import *

v1 = table.find_one(name='Jack Bauer')
v2 = table.find(belongs='CTU')
v3 = table.find(id=[1, 3, 5])

def func1():
    for p in table.find(belongs='CTU'):
        print(p)

def func2():
    for p in table.find(id=[1, 3, 5]):
        print(p)

# print(v1)
# print(v2)
# func1()
# print(v3)
# func2()
