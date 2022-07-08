from marshalldb import *
from pprint import pprint

v1 = Dictish([Pair("a", 1), Pair("pi", 3.14)])
v2 = !cat datadir/marshalldb.yml

v3 = list()
v4 = Dictish(v3)
v5 = v4.contents

# pprint(v1)
# pprint(v2)
# pprint(v3)
# pprint(v4)
