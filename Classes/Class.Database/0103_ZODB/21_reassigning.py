from zodb_mydata import *
import transaction

member = root.member
member[0] = 'Adam'
root.member = member
v1 = member
transaction.commit()
connection.close()

connection = ZODB.connection('mydata.fs')
root = connection.root
v2 = root.member
connection.close()

# print(v1)
# print(v2)
