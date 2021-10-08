from cerberus import Validator

schema = {'list_of_values': {
             'type': 'list',
             'items': [{'type': 'string'}, {'type': 'integer'}]}
          }
v = Validator(schema)

document = {'list_of_values': ['hello', 100]}
c1 = (v.validate(document), v.errors)
assert c1[0] == True

document = {'list_of_values': [100, 'hello']}
c2 = (v.validate(document), v.errors)
assert c2[0] == False
assert c2[1] == {'list_of_values':
                 [{0: ['must be of string type'],
                   1: ['must be of integer type']}]}
