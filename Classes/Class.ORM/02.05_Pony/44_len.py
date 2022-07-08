from university1 import *
from pprint import pprint

v1 = Student.select(lambda s: len(s.courses) > 2)

def func(data):
    for d in data:
        pprint(f'{d.name} {d.courses}')

# print(v1)
# func(v1)
