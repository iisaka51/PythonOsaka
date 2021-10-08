from cerberus import Validator

v = Validator({}, allow_unknown={'rename_handler': int})

document = {'0': 'foo'}
c1 = v.normalized(document)

keys = c1.keys()
assert (0 in keys) == True
assert ('0' in keys) == False
assert c1 != document
assert c1 == {0: 'foo'}

even_digits = lambda x: '0' + x if len(x) % 2 else x
v = Validator({}, allow_unknown={'rename_handler': [str, even_digits]})

document = {1: 'foo'}
c2 = v.normalized(document)

keys = c2.keys()
assert (1 in keys) == False
assert ('1' in keys) == False
assert ('01' in keys) == True
assert c2 != document
assert c2 == {'01': 'foo'}
