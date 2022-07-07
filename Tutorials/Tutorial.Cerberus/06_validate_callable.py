from cerberus import Validator

schema = {'name': {'type': 'string'},
           'age': {'type': 'integer', 'min': 10}}
document = {'name': 'David Coverdale', 'age': 70}

v = Validator(schema)
c = v(document)
assert c == True
