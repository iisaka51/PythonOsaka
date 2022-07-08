from notedb import *

v1 = Note.select().where(Note.text == 'Went to buy beer').get()
v2 = Note.get(Note.text == 'Eating pizza')

def print_obj(data):
    print(data.id)
    print(data.text)
    print(data.created)

# print_obj(v1)
# print_obj(v2)
