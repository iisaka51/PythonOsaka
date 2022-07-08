from tinydb_setup import *

test_john =  lambda n: n == 'John'

v1 = db.search(user.name.test(test_john))

# pprint(v1)
