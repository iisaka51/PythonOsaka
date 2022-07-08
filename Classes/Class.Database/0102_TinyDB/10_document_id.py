from tinydb_setup import *

v1 = db.get(user.name == 'John')
v2 = db.all()[0]
v3 = db.all()[-1]

# print(v1.doc_id, v1)
# print(v2.doc_id, v2)
# print(v3.doc_id, v3)
