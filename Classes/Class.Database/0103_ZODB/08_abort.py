from zodb_mydata import *
import transaction

root.member = ['Adam', 'Brian', 'John', 'Roger']

transaction.abort()
connection.close()
