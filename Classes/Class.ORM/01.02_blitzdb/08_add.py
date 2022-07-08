from model_beerdb import *

beer = Beer({'name': 'Hysteric IPA', 'abv': 7.0, 'stock': 6})
brewery = Brewery({'name': 'Y.Market', 'country': 'Japan'})

backend.save(beer)
backend.save(brewery)
backend.commit()

v1 = backend.get(Beer,{'name' : 'Hysteric IPA'})

# print(v1)
