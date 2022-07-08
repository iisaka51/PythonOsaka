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
v3 = Note.insert(text='Went to buy Wine').execute()
after_insert = Note.select()
v4 = func(after_insert)

v5 = Note.delete().where(Note.id > 4).execute()

after_delete = Note.select()
v6 = func(after_delete)

# pprint(v1)
# ...
# pprint(v5)
