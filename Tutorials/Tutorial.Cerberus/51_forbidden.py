from cerberus import Validator

schema = {'user': {'forbidden': ['root', 'admin']}}
v = Validator(schema)

document = {'user': 'root'}
c1 = (v.validate(document), v.errors)
assert c1[0] == False
assert c1[1] == {'user': ['unallowed value root']}

document = {'user': 'jack'}
c2 = (v.validate(document), v.errors)
assert c2[0] == True
