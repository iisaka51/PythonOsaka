from testdb import *

v1 = table.find(age=0)
v2 = table.find(age={'=': '0'})

def func(data):
    for d in data:
        print(d)

# func(v1)
