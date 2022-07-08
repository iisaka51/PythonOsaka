from testdb import *

people = db(person).select(orderby=person.name,
                    groupby=person.name, limitby=(0,100))

# print(people)
