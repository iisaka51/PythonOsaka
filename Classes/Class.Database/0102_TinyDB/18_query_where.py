from tinydb_setup import *

v1 = db.search(where('country-code') == 'USA')

# pprint(v1)
