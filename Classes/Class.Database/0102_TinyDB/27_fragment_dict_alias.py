from tinydb_setup import *

v1 = db.search((Query().name == 'John') & (Query()['country-code'] == 'GB'))

# pprint(v1)
