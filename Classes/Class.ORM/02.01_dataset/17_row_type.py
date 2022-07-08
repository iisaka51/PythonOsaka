import dataset
from usermodel import User

db = dataset.connect('sqlite:///users.sqlite', row_type=User)
table = db['users']

v1 = table.all()

def func(data):
    for user in data:
        print(user, f'  name="{user.name}"')

# print(v1)
# func(v1)
