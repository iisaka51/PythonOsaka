from model_beerdb import *
from pprint import pprint

v1 = backend.filter(Beer, {'name': 'ICHII SENSHIN', 'abv': 6.5})
v2 = backend.filter(Beer, {'$and': [{ 'name': 'ICHII SENSHIN' },
                                    { 'abv': 6.5 }]})

def show(data):
    for d in data:
        pprint(d)

# show(v1)
# show(v2)
