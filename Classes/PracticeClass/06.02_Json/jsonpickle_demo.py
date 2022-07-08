import json
import jsonpickle
from Beer import Beer

beer = Beer()
serialized = jsonpickle.encode(beer)
print(serialized)

beer_obj = jsonpickle.decode(serialized)
print(beer_obj.drink())
