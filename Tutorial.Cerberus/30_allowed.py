from cerberus import Validator

schema_list = {'role': {'type': 'list',
                        'allowed': ['agent', 'client', 'supplier']}}
schema_string = {'role': {'type': 'string',
                          'allowed': ['agent', 'client', 'supplier']}}
schema_integer = {'a_restricted_integer': {'type': 'integer',
                                           'allowed': [-1, 0, 1]}}
v = Validator()

v.schema = schema_list
c1 = (v.validate({'role': ['agent', 'supplier']}), v.errors)
assert c1[0] == True

c2 = (v.validate({'role': ['intern']}), v.errors)
assert c2[0] == False
assert c2[1] == {'role': ["unallowed values ('intern',)"]}

v.schema = schema_string
c3 = (v.validate({'role': 'supplier'}), v.errors)
assert c3[0] == True

c4 = (v.validate({'role': 'intern'}), v.errors)
assert c4[0] == False
assert c4[1] == {'role': ['unallowed value intern']}

v.schema = schema_integer
c5 = (v.validate({'a_restricted_integer': -1}), v.errors)
assert c5[0] == True

c6 = (v.validate({'a_restricted_integer': 2}), v.errors)
assert c6[0] == False
assert c6[1] == {'a_restricted_integer': ['unallowed value 2']}
