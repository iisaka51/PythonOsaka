from testdb import *

Person._connection.debug = True

p = Person(firstName='Freddie', lastName='Mercury')
p.set(firstName='Adam', lastName='Lambert')

# print(p)
