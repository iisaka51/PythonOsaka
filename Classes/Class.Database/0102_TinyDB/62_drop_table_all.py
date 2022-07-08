from tinydb_usersetup import *

database_initialized()

v1 = db.tables()
db.drop_table('group')
v2 = db.tables()

table_devision = db.table('devision')
table_role = db.table('role')

v3 = db.tables()
table_devision.insert({'name': 'devops'})
table_role.insert({'name': 'manager'})
v4 = db.tables()

db.default_table_name = 'role'
v5 = db.tables()
db.drop_tables()
v6 = db.tables()

# pprint(v1)
# pprint(v2)
# pprint(v3)
# pprint(v4)
# pprint(v5)
# pprint(v6)

