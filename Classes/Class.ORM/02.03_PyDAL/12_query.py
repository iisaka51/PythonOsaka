from testdb import *

query1 = (person.belongs == 'Heart') & (person.name.startswith('A'))
ann = db(query1).select(person.ALL)
query2 = person.age > 70
elderly = db(query2).select(person.ALL)

# print(query1)
# print(ann)
# print(query2)
# print(elderly)
