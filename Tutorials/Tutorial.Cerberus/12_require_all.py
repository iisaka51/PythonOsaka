from cerberus import Validator

schema = {'name': {'type': 'string'},
           'age': {'type': 'integer', 'min': 10}}
document = {'name': 'David Coverdale'}

v = Validator(schema)
assert v.require_all == False

c1 = (v(document), v.errors)
assert c1[0] == True

v.require_all = True

c2 = (v(document), v.errors)
assert c2[0] == False
assert c2[1] == {'age': ['required field']}
