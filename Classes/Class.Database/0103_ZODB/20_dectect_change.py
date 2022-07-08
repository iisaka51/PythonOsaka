from zodb_mydata import *
import transaction


root.member = ['Freddie', 'Brian', 'John', 'Roger']
transaction.commit()
connection.close()


connection = ZODB.connection('mydata.fs')
root = connection.root
v1 = root.member
root.member[0] = 'Adam'
transaction.commit()
v2 = root.member
connection.close()

connection = ZODB.connection('mydata.fs')
root = connection.root
v3 = root.member
connection.close()

# print(v1)
# print(v2)
# print(v3)
