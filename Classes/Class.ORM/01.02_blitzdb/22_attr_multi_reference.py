from model_beerdb import *
from pprint import pprint

v1 = backend.filter(Beer, {'$and': [{ 'abv': { '$gte': 5.5 }},
                                    { 'abv': { '$lte': 7.0 }}]})

def show(data):
    for d in data:
        pprint(d)

# show(v1)
