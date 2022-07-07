from cerberus import Validator

schema = {'a_dict': {
              'type': 'dict',
              'keysrules': {'type': 'string', 'regex': '[a-z]+'}}
          }
v = Validator(schema)

document = {'a_dict': {'key': 'value'}}
c1 = (v.validate(document), v.errors)
assert c1[0] == True

document = {'a_dict': {'KEY': 'value'}}
c2 = (v.validate(document), v.errors)
assert c2[0] == False
assert c2[1] == {'a_dict':
                 [{'KEY': ["value does not match regex '[a-z]+'"]}]}
