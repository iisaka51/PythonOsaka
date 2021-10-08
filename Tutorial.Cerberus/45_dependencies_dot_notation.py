from cerberus import Validator

schema = {
    'test_field': {'dependencies': ['a_dict.foo', 'a_dict.bar']},
    'a_dict': {
        'type': 'dict',
        'schema': {
            'foo': {'type': 'string'},
            'bar': {'type': 'string'}
        }
    }
}

document = {'test_field': 'foobar',
            'a_dict': {'foo': 'foo'}}

v = Validator()

c = (v.validate(document, schema), v.errors)
assert c[0] == False
assert c[1] == {'test_field': ["field 'a_dict.bar' is required"]}
