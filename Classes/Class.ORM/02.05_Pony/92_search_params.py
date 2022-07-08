from example import *
from ponywhoosh import search
from pprint import pprint

v1 = search(Student, "smith", include_entity=True, use_dict=False)
v2 = search(Student, "smith", include_entity=True, use_dict=True)

# pprint(v1)
# pprint(v2)
