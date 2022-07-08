from testdb import *

v1 = table.find(belongs=('Pink Floyd', 'Hear'))
v2 = table.find(belongs={'in': ('Pink Floyd', 'Hear')})

def func(data):
    for d in data:
        print(d)

# func(v1)
