from cerberus import Validator

document = {'states': ['peace', 'love', 'inity']}
schema = {'states': {'contains': 'peace'}}

v = Validator()

c1 = (v.validate(document, schema), v.errors)
assert c1[0] == True

schema = {'states': {'contains': 'greed'}}
c2 = (v.validate(document, schema), v.errors)
assert c2[0] == False
assert c2[1] == {'states': ["missing members {'greed'}"]}

schema = {'states': {'contains': ['love', 'inity']}}
c3 = (v.validate(document, schema), v.errors)
assert c3[0] == True

schema = {'states': {'contains': ['love', 'respect']}}
c4 = (v.validate(document, schema), v.errors)
assert c4[0] == False
assert c4[1] == {'states': ["missing members {'respect'}"]}
