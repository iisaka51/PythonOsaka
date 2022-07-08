from example import *
from ponywhoosh import search
from pprint import pprint

v1 = search(Student,"s", add_wildcards=True, sortedby="gpa")

# pprint(v1)
