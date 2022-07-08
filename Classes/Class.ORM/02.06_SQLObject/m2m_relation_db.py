from sqlobject import *
import os

db_filename = os.path.abspath('m2m_rel.db')
connection_string = 'sqlite:' + db_filename
connection = connectionForURI(connection_string)
sqlhub.processConnection = connection

class User(SQLObject):

    class sqlmeta:
        table = "user_table"

    username = StringCol(alternateID=True, length=20)
    roles = RelatedJoin('Role')

class Role(SQLObject):

    name = StringCol(alternateID=True, length=20)
    users = RelatedJoin('User')

if __name__ == '__main__':
    User.createTable()
    Role.createTable()
