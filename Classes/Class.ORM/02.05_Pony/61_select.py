from university1 import *

sql_debug(True)
v1 = select(s for s in Student)

def func(data):
    for d in data:
        print(f'{d.name} {d.gpa}')

# print(v1)
# func(v1)
