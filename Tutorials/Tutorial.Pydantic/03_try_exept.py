from model_user import User
from pydantic import ValidationError

data = { 'id': 'CTU Agent',
         'username': 'Jack Bauer',
         'password': 'Password123',
         'confirm_password': 'Password123',
         'email': 'jack@ctu.com',
         'timestamp': '2021-08-24 20:30',
         'friends': [1, '2', b'3']
       }

try:
    user = User(**data)
    msg = ''
except ValidationError as e:
    user = None
    msg = e.json()

# print(user)
# print(mg)
