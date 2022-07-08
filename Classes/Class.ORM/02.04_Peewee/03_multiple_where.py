from notedb import *

notes = Note.select().where((Note.id > 1) & (Note.id < 4))

def func(data):
    for d in data:
        print(f'{d.id} {d.text} {d.created}' )

# func(notes)
