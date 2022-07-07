from cerberus import schema_registry, Validator

schema_registry.add('non-system user',
                    {'uid': {'min': 1000, 'max': 0xffff}})

schema = {'sender': {'schema': 'non-system user',
                     'allow_unknown': True},
          'receiver': {'schema': 'non-system user',
                       'allow_unknown': True}}

v = Validator(schema)

document = {'sender': {'uid': 0}}
c1 = (v.validate(document), v.errors)
assert c1[0] == False
assert c1[1] == {'sender': [{'uid': ['min value is 1000']}]}

document = {'sender': {'uid': 1000}}
c2 = (v.validate(document), v.errors)
assert c2[0] == True

document = {'sender': {'uid': 1001}}
c3 = (v.validate(document), v.errors)
assert c3[0] == True
