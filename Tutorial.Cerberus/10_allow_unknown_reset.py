from cerberus import Validator


schema = {'name': {'type': 'string'},
           'age': {'type': 'integer', 'min': 10}}
document = {'name': 'David Coverdale', 'country': 'USA'}

v = Validator(schema)
assert v.allow_unknown == False

v.allow_unknown = True
c1 = (v.validate(document), v.errors)
assert c1[0] == True

v.allow_unknown = False
c2 = (v.validate(document), v.errors)
assert c2[0] == False
assert c2[1] == {'country': ['unknown field']}
