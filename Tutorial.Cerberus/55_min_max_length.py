from cerberus import Validator

schema = {'numbers': {'minlength': 1, 'maxlength': 3}}
v = Validator(schema)

document = {'numbers': [256, 2048, 23]}
c1 = (v.validate(document), v.errors)
assert c1[0] == True

document = {'numbers': [256, 2048, 23, 2]}
c2 = (v.validate(document), v.errors)
assert c2[0] == False
assert c2[1] == {'numbers': ['max length is 3']}
