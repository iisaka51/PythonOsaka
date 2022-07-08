from notedb import *

notes = Note.select()

def func(data):
    for d in data:
        print(f'{d.text} {d.created}' )

# func(notes)
