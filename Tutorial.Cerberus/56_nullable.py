from cerberus import Validator

schema = {'a_nullable_integer': {'type': 'integer','nullable': True},
          'an_integer': {'type': 'integer'}}
v = Validator(schema)

document = {'a_nullable_integer': 3}
c1 = v.validate(document)
assert c1 == True

document = {'a_nullable_integer': None}
c2 = v.validate(document)
assert c2 == True

document = {'an_integer': 3}
c3 = v.validate(document)
assert c3 == True

document = {'an_integer': None}
c4 = (v.validate(document), v.errors)
assert c4[0] == False
assert c4[1] == {'an_integer': ['null value not allowed']}
