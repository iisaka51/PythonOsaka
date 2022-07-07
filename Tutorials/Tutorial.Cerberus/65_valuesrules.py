from cerberus import Validator

schema = {'numbers':
             {'type': 'dict',
              'valuesrules': {'type': 'integer', 'min': 10}}
}

v = Validator(schema)

document = {'numbers': {'an integer': 10, 'another integer': 100}}
c = v.validate(document)
assert c == True

document = {'numbers': {'an integer': 9}}
c = (v.validate(document), v.errors)
assert c[0] == False
assert c[1] == {'numbers': [{'an integer': ['min value is 10']}]}
