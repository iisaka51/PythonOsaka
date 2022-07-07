from cerberus import Validator

schema = {'name': {'type': 'string'},
           'age': {'type': 'integer', 'min': 10}}

v = Validator(schema)

v.schema = {}
v.allow_unknown = {'type': 'string'}
document = {'an_unknown_field': 'john'}
c1 = (v.validate(document), v.errors)
assert c1[0] == True

document = {'an_unknown_field': 1}
c2 = (v.validate(document), v.errors)
assert c2[0] == False
assert c2[1] == {'an_unknown_field': ['must be of string type']}
