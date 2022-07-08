from cerberus import Validator, DocumentError
from datetime import datetime

v = Validator()
to_date = lambda s: datetime.strptime(s, '%Y-%m-%d')
v.schema = {
    'id': {'type': 'integer', 'min': 1 },
    'username': {
        'type': 'string',
        'minlength': 8, 'maxlength': 20 },
    'email': {
        'type': 'string',
        'regex': "^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$" },
    'birthday': {'type': 'date', 'coerce': to_date },
    'age': {'type': 'integer', 'min': 0},
    }


user1 =  dict( id=1, username="Jack Johnson",
              email="jackJohnson@gmail.com",
              birthday='1970-07-20', age=52  )
user2 =  dict( id=2, username="Goichi (iisaka) Yukawa",
               email="iisaka51@gmail.",
               birthday='1962-01-13', age=-20 )

try:
    if not v.validate(user1):
        print(v.errors)
    if not v.validate(user2):
        print(v.errors)
except DocumentError as e:
    print(e)
