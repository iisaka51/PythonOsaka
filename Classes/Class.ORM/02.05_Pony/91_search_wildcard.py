from example import *
from ponywhoosh import search
from pprint import pprint

v1 = search(Student, "s", add_wildcards=False)
v2 = search(Student, "s", add_wildcards=True)

# pprint(v1)
# pprint(v2)
