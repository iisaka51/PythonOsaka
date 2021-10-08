from cerberus import Validator

schema = {'a_dict': {'type': 'dict',
                     'schema': {'address': {'type': 'string'},
                                'city': {'type': 'string',
                                         'required': True}}
                    }
        }

v = Validator(schema)

document = {'a_dict': {'address': 'my address', 'city': 'my town'}}
c = v.validate(document)
assert c == True
