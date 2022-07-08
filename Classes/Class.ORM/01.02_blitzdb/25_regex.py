from model_beerdb import *
from pprint import pprint

def show(data):
    for d in data:
        pprint(d)
    else:
        print('None')


query1 = {'name': {'$regex': '.*Ale$'}}

v1 = backend.filter(Beer, query1)

# show(v1)
