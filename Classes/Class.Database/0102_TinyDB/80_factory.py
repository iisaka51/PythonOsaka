from tinydb_usersetup import *
from tinydb_base import Factory

database_initialized()

db = Factory('usergroup.json', 'group')
v1 = db.db          # TinyDBとおなじ
v2 = db.tbl         # TinyDB.Tableとおなじ
v3 = db.tbl.search(Query()['name'] == 'John')

# print(v1)
# print(v2)
# print(v3)
# db.close()
