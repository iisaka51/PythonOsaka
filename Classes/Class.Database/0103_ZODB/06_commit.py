from zodb_mydata import *
import transaction

root.member = ['Freddie', 'Brian', 'John', 'Roger']

transaction.commit()
connection.close()
