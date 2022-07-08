from one_relationdb import *

v1 = db(db.car.owner_id == 1).select()
v2 = db(db.car.name == 'Mustang Cobra').select()

# print(v1)
# print(v2)
