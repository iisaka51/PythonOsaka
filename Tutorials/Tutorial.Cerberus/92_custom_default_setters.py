from cerberus import Validator
from datetime import datetime

class MyNormalizer(Validator):
    def _normalize_default_setter_utcnow(self, document):
        return datetime.utcnow()
    def _normalize_default_setter_anniversary(self, document):
        return datetime(2020, 10, 2)

schema = {'creation_date': {'type': 'datetime',
                            'default_setter': 'anniversary'}}

c = MyNormalizer().normalized({}, schema)
assert c == {'creation_date': datetime(2020, 10, 2, 0, 0)}
