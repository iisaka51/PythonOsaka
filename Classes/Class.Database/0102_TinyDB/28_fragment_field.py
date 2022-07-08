from tinydb_setup import *

test_d1 = {'year': 1946, 'month': 9, 'day': 5}
test_d2 = {'month': 7}

v1 = db.search(Query().birthday.fragment(test_d1))
v2 = db.search(Query().birthday.fragment(test_d2))

# pprint(v1)
# pprint(v2)
