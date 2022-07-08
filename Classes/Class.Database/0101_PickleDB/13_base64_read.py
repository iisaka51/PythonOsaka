import pickledb
import pickle
import base64
from pprint import pprint

db=pickledb.load('sample.db',False)

base64_data = db.get('foo')
serial_data = base64.b64decode(base64_data)
data = pickle.loads(serial_data)

# pprint(base64_data)
# pprint(serial_data)
# pprint(data)
