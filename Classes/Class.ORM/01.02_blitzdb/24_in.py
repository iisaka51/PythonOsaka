from model_beerdb import *
from pprint import pprint

def show(data):
    for d in data:
        pprint(d)
    else:
        print('None')


query1 = {'name': {'$in': ['Ale']}}
query2 = {'name': {'$not': {'$in': ['Ale']}}}

v1 = backend.filter(Beer, query1)
v2 = backend.filter(Beer, query2)

# show(v1)
# show(v2)
