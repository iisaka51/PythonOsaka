import re
from tinydb_setup import *

v1 = db.search(user.name.matches('john', flags=re.IGNORECASE))

# pprint(v1)
