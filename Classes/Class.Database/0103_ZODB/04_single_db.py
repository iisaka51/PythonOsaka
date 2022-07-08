import ZODB

connection = ZODB.connection('mydata.fs')
memory_connection = ZODB.connection(None)
