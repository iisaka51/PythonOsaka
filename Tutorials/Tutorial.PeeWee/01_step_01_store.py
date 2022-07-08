from models import *
from datetime import date

uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15))
v1 = uncle_bob.save()

# print(uncle_bob)
# print(v1)
