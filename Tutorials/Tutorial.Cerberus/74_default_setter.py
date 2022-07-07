from cerberus import Validator

v = Validator()
v.schema = {'a': {'type': 'integer'},
            'b': {'type': 'integer',
            'default_setter': lambda doc: doc['a'] + 1}}


c1 = v.normalized({'a': 1})
assert c1 == {'a': 1, 'b': 2}

v.schema = {'a': {'type': 'integer',
                  'default_setter': lambda doc: doc['not_there']}}

c = v.normalized({})
assert c == None
assert v.errors == {'a': ["default value for 'a' cannot be set: Circular dependencies of default setters."]}
