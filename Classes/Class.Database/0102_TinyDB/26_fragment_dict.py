from tinydb_setup import *

test_d = {'name': 'John', 'country-code': 'GB'}
v1 = db.search(Query().fragment(test_d))

pprint(v1)
