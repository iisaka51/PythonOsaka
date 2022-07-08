from tinydb_setup import *

database_initialized()

before_data = db.all()

db.update({'current_member': 1}, doc_ids=[3,4])
db.remove(doc_ids=[1,2])

after_data = db.all()

check = db.contains(doc_id=1)
doc = db.get(doc_id=3)

# pprint(check)
# pprint(before_data)
# pprint(after_data)
# pprint(doc)
