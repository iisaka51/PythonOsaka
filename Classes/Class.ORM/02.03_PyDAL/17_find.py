from testdb import *

people = db().select(db.person.ALL)
v1 = f'{people}'

v2 = people.find(lambda row: row.belongs == 'Heart')
v3 = people.exclude(lambda row: row.belongs == 'Heart')
v4 = people.sort(lambda row: row.name)

# print(v1)
# print(v2)
# print(v3)
# print(people)
