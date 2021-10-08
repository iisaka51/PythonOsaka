from cerberus import Validator

schema = {'weight': {'min': 10.1, 'max': 10.9}}

v = Validator(schema)

document = {'weight': 10.3}
c1 = (v.validate(document), v.errors)
assert c1[0] == True

document = {'weight': 12}
c2 = (v.validate(document), v.errors)
assert c2[0] == False
assert c2[1] == {'weight': ['max value is 10.9']}
