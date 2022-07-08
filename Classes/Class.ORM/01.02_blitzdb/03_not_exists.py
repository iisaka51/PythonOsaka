from model_beerdb import *

try:
    v1 = backend.get(Beer,{'name' : 'Hysteric IPA'})
    msg = ''
except Beer.DoesNotExist as e:
    v1 = None
    msg = e

# print(v1)
# print(msg)
