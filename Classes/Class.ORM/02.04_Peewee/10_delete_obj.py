from notedb import *
from pprint import pprint

def func(data):
    output = list()
    for d in data:
        output.append(f'{d.id} {d.text} {d.created}' )
    return output

before_data = Note.select()
v1 = func(before_data)
v2 = Note.insert(text='Watching YouTube.com').execute()
after_insert = Note.select()
v3 = func(after_insert)

v4 = Note.delete_by_id(5)

after_delete = Note.select()
v5 = func(after_delete)

# pprint(v1)
# ...
# pprint(v5)
