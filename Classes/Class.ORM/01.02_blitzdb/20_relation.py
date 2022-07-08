from model_beerdb import *
from pprint import pprint

plank = backend.get(Brewery, {'name': 'Plank'})
pilserl = backend.get(Beer, {'name': 'Pilserl'})

pilserl.brewery = plank

# pprint(pilserl)
# print(pilserl.brewery.country)
