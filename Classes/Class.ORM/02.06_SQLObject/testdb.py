from sqlobject import *
import os

db_filename = os.path.abspath('test.db')
connection_string = 'sqlite:' + db_filename
connection = connectionForURI(connection_string)
sqlhub.processConnection = connection

class Person(SQLObject):

    firstName = StringCol()
    middleInitial = StringCol(length=1, default=None)
    lastName = StringCol()

if __name__ == '__main__':
    Person.createTable()
    d = Person(firstName="John", lastName="Doe")
