from cerberus import Validator, SchemaError

schema = {'foo': {'allowed': []}}
v = Validator(schema)


try:
    v.schema['foo'] = {'allowed': 1}
except SchemaError as e:
    print(f'1st: {e}')

v.schema['foo']['allowed'] = 'strings are no valid constraint for allowed'

try:
    v.schema.validate()
except SchemaError as e:
    print(f'2nd: {e}')
