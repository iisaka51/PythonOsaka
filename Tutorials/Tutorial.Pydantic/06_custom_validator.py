from model_user2 import *
from test_data import test_data
from pprint import pprint

def func():
    for d in test_data:
        try:
            user = User(**d)
        except ValidationError as e:
            user = e
        print(f'{d["comment"]} - {d["username"]}:')
        pprint(f'{user}')

# func()
