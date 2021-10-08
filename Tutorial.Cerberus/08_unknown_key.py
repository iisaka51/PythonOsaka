from cerberus import Validator

schema = {'name': {'type': 'string'},
           'age': {'type': 'integer', 'min': 10}}
document = {'name': 'David Coverdale', 'country': 'USA'}

v = Validator(schema)
assert v.allow_unknown == False

c1 = (v.validate(document), v.errors)
assert c1[0] == False
assert c1[1] == {'country': ['unknown field']}

v.allow_unknown = True

c2 = (v.validate(document), v.errors)
assert c2[0] == True
