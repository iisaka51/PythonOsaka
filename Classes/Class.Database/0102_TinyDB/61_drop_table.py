from tinydb_usersetup import *

database_initialized()

v1 = db.tables()
v2 = db_group.all()
v3 = db.drop_table('group')
v4 = db_group.all()

# pprint(v1)
# pprint(v2)
# pprint(v3)
# pprint(v4)
