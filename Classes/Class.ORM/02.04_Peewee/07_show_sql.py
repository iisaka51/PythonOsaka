from notedb import *

v1 = Note.select().where(Note.id == 3)
v2 = v1.sql()

# print(v1)
# print(v2)
