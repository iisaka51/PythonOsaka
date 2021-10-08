from cerberus import Validator

schema = {'name': {'required': True, 'type': 'string'},
            'age': {'type': 'integer'}}

v = Validator(schema)

document = {'age': 10}
c1 = (v.validate(document), v.errors)
assert c1[0] == False
assert c1[1] == {'name': ['required field']}

c2 = v.validate(document, update=True)
assert c2 == True
