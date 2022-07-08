import pickledb
import pickle
import base64
from pprint import pprint

db=pickledb.load('sample.db',False)

data={1:1, 2:2, 3:3}

serial_data = pickle.dumps(data)
base64_data = base64.b64encode(serial_data).decode('utf-8')
db.set('foo', base64_data)

# pprint(base64_data)
# db.dump()
