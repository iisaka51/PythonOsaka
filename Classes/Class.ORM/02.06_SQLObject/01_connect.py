from sqlobject import *
import os

db_filename = os.path.abspath('test.db')
connection_string = 'sqlite:' + db_filename
connection = connectionForURI(connection_string)
sqlhub.processConnection = connection
