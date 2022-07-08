from notedb import *

v1 = (Note
      .select(Note.text, Note.created)
      .order_by(Note.created))
v2 = (Note
      .select(Note.text, Note.created)
      .order_by(Note.created.desc()))

def func(data):
    for d in data:
        print(f'{d.text} {d.created}' )

# func(v1)
# func(v2)
