from tinydb_setup import *

v1 = db.update_multiple([
  ({'current_member': 0}, where('name') == 'John'),
  ({'current_member': 0}, where('name') == 'Freddie'),
  ({'current_member': 1}, where('name') == 'Brian'),
  ({'current_member': 1}, where('name') == 'Roger'),
])

v2 = db.all()

# pprint(v1)
# pprint(v2)
