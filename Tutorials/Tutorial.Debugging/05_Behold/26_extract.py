# now debugging...

from behold import Behold
from database import db, table
from models import User

class CustomBehold(Behold):
    def load_state(self):
        self.lookup = your_lookup_code()

    def extract(self, item, name):
        if hasattr(item, id):
            val = getattr(item, name)
            if isinstance(item, User):
                return self.lookup.get(val, '')
            else:
                return super(CustomBehold, self).extract(name, item)
        else:
            return ''

for user in table.all():
    _ = CustomBehold().when(name='David Gilmour').show('id')
