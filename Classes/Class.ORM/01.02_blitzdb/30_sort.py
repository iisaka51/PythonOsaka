from model_beerdb import *
from blitzdb.queryset import QuerySet
from pprint import pprint

def show(data):
    for d in data:
        pprint(d)

v1 = backend.filter(Beer, {}).sort([("abv", QuerySet.ASCENDING)])
v2 = backend.filter(Beer, {}).sort([("abv", QuerySet.DESCENDING)])

# show(v1)
# show(v2)
