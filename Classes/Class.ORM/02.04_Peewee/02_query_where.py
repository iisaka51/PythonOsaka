from notedb import *

notes = Note.select().where(Note.id > 3)

def func(data):
    for d in data:
        print(f'{d.id} {d.text} {d.created}' )

# func(notes)
