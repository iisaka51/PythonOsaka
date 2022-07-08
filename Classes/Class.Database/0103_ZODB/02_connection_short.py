import ZODB

db = ZODB.DB('mydata.fs')
connection = db.open()
root = connection.root
