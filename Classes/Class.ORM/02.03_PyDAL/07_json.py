from testdb import *
from pprint import pprint

v1 = db().select(db.person.ALL)
v2 = v1.as_csv()
v3 = v1.as_json()
v4 = v1.as_list()
v5 = v1.as_dict()
v6 = v1.as_xml()

# print(v1)
# print(v2)
# pprint(v3)
# pprint(v4)
# pprint(v5)
# pprint(v6)
