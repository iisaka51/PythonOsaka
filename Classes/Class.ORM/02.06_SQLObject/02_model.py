class Person(SQLObject):

    firstName = StringCol()
    middleInitial = StringCol(length=1, default=None)
    lastName = StringCol()

# Person.createTable()
