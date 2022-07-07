from cerberus import Validator

class MyNormalizer(Validator):
    def __init__(self, multiplier, *args, **kwargs):
        super(MyNormalizer, self).__init__(*args, **kwargs)
        self.multiplier = multiplier

    def _normalize_coerce_multiply(self, value):
        return value * self.multiplier

schema = {'foo': {'coerce': 'multiply'}}
document = {'foo': 2}

c = MyNormalizer(2).normalized(document, schema)
assert c == {'foo': 4}
