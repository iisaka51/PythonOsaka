from sqlobject import *
import os

db_filename = os.path.abspath('one_rel.db')
connection_string = 'sqlite:' + db_filename
connection = connectionForURI(connection_string)
sqlhub.processConnection = connection

class Address(SQLObject):

    street = StringCol()
    city = StringCol()
    state = StringCol(length=2)
    zip = StringCol(length=9)
    person = ForeignKey('Person')

class Person(SQLObject):

    firstName = StringCol()
    middleInitial = StringCol(length=1, default=None)
    lastName = StringCol()
    address = MultipleJoin('Address')


if __name__ == '__main__':
    Address.createTable()
    Person.createTable()
    d = Person(firstName="John", lastName="Doe")
