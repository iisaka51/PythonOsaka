from cerberus import Validator

schema = {'prop1':
            {'type': 'number',
             'anyof': [{'min': 0, 'max': 10},
                       {'min': 100, 'max': 110}]
            }
        }

v = Validator(schema)

document = {'prop1': 5}
c = v.validate(document)
assert c == True

document = {'prop1': 105}
c = v.validate(document)
assert c == True

document = {'prop1': 55}
c = (v.validate(document), v.errors)
assert c[0] == False
assert c[1] == {'prop1': ['no definitions validate',
                 {'anyof definition 0': ['max value is 10'],
                  'anyof definition 1': ['min value is 100']}]}
