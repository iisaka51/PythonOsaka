from notedb import *
from pprint import pprint

def func(data):
    output = list()
    for d in data:
        output.append(f'{d.id} {d.text} {d.created}' )
    return output

before_update = Note.select()
v1 = func(before_update)

v2 = (Note
      .update(created=datetime.date(2021, 8, 8))
      .where(Note.id == 1)
      .execute())

after_update = Note.select()
v3 = func(after_update)

# pprint(v1)
# pprint(v2)
# pprint(v3)
