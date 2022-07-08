from beerdb import *

v1 = Drink.objects.filter(data__abv=4.9)
v2 = list(v1)

# print(v1)
# print(v2)
# Drink.objects.filter(data__abv==4.9)
