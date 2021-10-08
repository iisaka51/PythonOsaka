from cerberus import Validator

schema = {
    'test_field': {},
    'a_dict': {
        'type': 'dict',
        'schema': {
            'foo': {'type': 'string'},
            'bar': {'type': 'string',
                    'dependencies': '^test_field'}
        }
    }
}

v = Validator()
document = {'a_dict': {'bar': 'bar'}}
c = (v.validate(document, schema), v.errors)
assert c[0] == False
assert c[1] == {'a_dict':
                [{'bar': ["field '^test_field' is required"]}]}
