from model_beerdb import *

try:
    v1 = backend.get(Beer,{'abv' : 5.5})
    msg = ''
except Beer.MultipleDocumentsReturned as e:
    v1 = None
    msg = e

# print(v1)
# print(msg)
