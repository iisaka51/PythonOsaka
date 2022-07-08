from notedb import *

v1 = Note.select().offset(2)
v2 = Note.select().limit(3)
v3 = Note.select().offset(2).limit(3)

def func(data):
    for d in data:
        print(f'{d.id} {d.text} {d.created}' )

# func(v1)
# func(v2)
# func(v3)
# print(v1)
# print(v2)
# print(v3)
