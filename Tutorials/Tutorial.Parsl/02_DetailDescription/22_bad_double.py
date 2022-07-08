import random
import parsl
from parsl.app.app import python_app

from htex_config import htex_config
conf = parsl.load(htex_config)

factor = 5

@python_app
def bad_double(x):
     return x * random.random() * factor

num = bad_double(42)
print(num.result())
