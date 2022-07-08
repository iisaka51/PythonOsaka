from model_beerdb import *
from pprint import pprint

def show(data):
    for d in data:
        pprint(d)
    else:
        print('None')

query1 = {'abv': {'$exists': True}}
query2 = {'abv': {'$exists': False}}
query3 = {'ibu': {'$exists': False}}

v1 = backend.filter(Beer, query1)
v2 = backend.filter(Beer, query2)
v3 = backend.filter(Beer, query3)

# show(v1)
# show(v2)
# show(v3)

