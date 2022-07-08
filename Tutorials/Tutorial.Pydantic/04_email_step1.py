from model_user3 import *

data = { 'id': '1001',
         'username': 'Jack Bauer',
         'password': 'Password123',
         'confirm_password': 'Password123',
         'email': 'jack@ctu.com',
         'timestamp': '2021-08-24 20:30',
         'friends': [1, '2', b'3']
       }

def func(user_data):
    try:
        user = User(**user_data)
    except ValidationError as e:
        user = None
        print(e)
    return user

user = func(data)
v1 = user.password
v2 = user.password == user.confirm_password

# print(user)
# print(v1)
# print(v2)
# print(type(user.password))
# user.password = 'python'
# print(user.password)
# print(type(user.password))
