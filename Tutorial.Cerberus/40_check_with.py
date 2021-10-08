from cerberus import Validator

def oddity(field, value, error):
    if not value & 1:
        error(field, "Must be an odd number")

schema = {'amount': {'check_with': oddity}}
v = Validator(schema)

c1 = (v.validate({'amount': 10}), v.errors)
assert c1[0] == False
assert c1[1] == {'amount': ['Must be an odd number']}

c2 = (v.validate({'amount': 9}), v.errors)
assert c2[0] == True
