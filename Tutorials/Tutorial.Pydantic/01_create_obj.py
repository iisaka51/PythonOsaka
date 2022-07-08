from model_user import User

data = { 'id': '1001',
         'username': 'Jack Bauer',
         'password': 'Password123',
         'confirm_password': 'Password123',
         'email': 'jack@ctu.com',
         'timestamp': '2021-08-24 20:30',
         'friends': [1, '2', b'3']
       }

user = User(**data)

# print(user)
