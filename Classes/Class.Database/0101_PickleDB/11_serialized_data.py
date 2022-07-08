import pickledb
import pickle
import base64
from pprint import pprint

db=pickledb.load('sample.db',False)

data={1:1, 2:2, 3:3}

serial_data = pickle.dumps(data)
db.set('foo', serial_data)

# pprint(serial_data)
# pprint(pickle.loads(db.get('foo')))
# pprint(type(pickle.loads(db.get('foo'))))

# db.dump()
