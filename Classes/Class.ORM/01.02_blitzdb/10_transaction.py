from model_beerdb import *
from pprint import pprint

def list_beers():
    for d in backend.filter(Beer, {}):
        print(f'{d.name} {d.abv}')

trans = backend.begin()
backend.get(Beer, {'name': 'Pale Ale'}).delete()
backend.rollback(trans)

backend.commit()

# list_beers()
