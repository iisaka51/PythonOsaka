import ZODB
from pprint import pprint

connection = ZODB.connection('mydata.fs')
root = connection.root
