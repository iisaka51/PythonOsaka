from notedb import *

v1 = Note.select().count()
v2 = (Note
      .select()
      .where(Note.created >= datetime.date(2021, 8, 20))
      .count())

# print(v1)
# print(v2)
