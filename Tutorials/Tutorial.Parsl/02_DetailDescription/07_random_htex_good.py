import parsl
from parsl.app.app import python_app
from htex_config import htex_config

parsl.clear()
conf = parsl.load(htex_config)

factor = 5

@python_app
def ambiguous_double(factor, x):
     import random
     return x * random.random() * factor

app = ambiguous_double(factor, 42)
print(app.result())
