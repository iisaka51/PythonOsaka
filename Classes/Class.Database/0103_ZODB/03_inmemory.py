import ZODB

db = ZODB.DB(None)
connection = db.open()
root = connection.root
