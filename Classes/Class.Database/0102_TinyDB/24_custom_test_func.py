import re
from tinydb_setup import *

def year_check(val, m, n):
    return m <= val < n

v1 = db.search(user.birthday.year.test(year_check, 1940, 1948))

# pprint(v1)
