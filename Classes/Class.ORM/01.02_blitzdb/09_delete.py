from model_beerdb import *
from pprint import pprint

def list_beers():
    for d in backend.filter(Beer, {}):
        print(f'{d.name} {d.abv}')

beer = backend.get(Beer, {'name': 'Pale Ale'})
backend.delete(beer)
backend.commit()

# pprint(beer)
# list_beers()
# backend.save(beer)
# backend.commit()
# list_beers()
