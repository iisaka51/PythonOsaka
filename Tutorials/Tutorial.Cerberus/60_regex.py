from cerberus import Validator

schema = {
    'email': {
       'type': 'string',
       'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    }
}

v = Validator(schema)

document = {'email': 'john@example.com'}
c = v.validate(document)
assert c == True

document = {'email': 'john_at_example_dot_com'}
c = (v.validate(document, schema), v.errors)
assert c[0] == False
assert c[1] ==  {'email':
["value does not match regex \
'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$'"]}
