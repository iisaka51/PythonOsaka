from cerberus import Validator

class MyValidator(Validator):
    def _validate_is_odd(self, constraint, field, value):
        """ Test the oddity of a value.

        The rule's arguments are validated against this schema:
        {'type': 'boolean'}
        """
        if constraint is True and not bool(value & 1):
            self._error(field, "Must be an odd number")

schema = {'amount': {'is odd': True, 'type': 'integer'}}

v = MyValidator(schema)
c = v.validate({'amount': 10})
assert c == False
assert v.errors == {'amount': ['Must be an odd number']}

c = v.validate({'amount': 9})
assert c == True
