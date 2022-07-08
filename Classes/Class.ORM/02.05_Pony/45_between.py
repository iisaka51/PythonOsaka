from estore import *

v1 = select(p for p in Customer if between(p.age, 18, 65))

def func(data):
    for d in data:
        print(f'{d.name}  {d.age}')

# print(v1)
# func(v1)
