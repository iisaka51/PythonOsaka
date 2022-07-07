from cerberus import rules_set_registry, Validator

rules_set_registry.extend((('boolean', {'type': 'boolean'}),
                           ('booleans', {'valuesrules': 'boolean'})))
schema = {'foo': 'booleans'}

v = Validator(schema)
r = v.rules['valuesrules']

c = v.validate({'foo': 1})
assert c == True

c = v.validate({'foo': True})
assert c == True

c = v.validate({'foo': {'enable': True}})
assert c == True

c = v.validate({'foo': {'name': 'Jack'}})
assert c == False
assert v.errors == {'foo': [{'name': ['must be of boolean type']}]}

# r
