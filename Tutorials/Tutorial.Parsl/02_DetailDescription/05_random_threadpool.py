import parsl
from parsl.app.app import python_app
import random
factor = 5

conf = parsl.load()

@python_app
def ambiguous_double(x):
     return x * random.random() * factor

app = ambiguous_double(42)
print(app.result())
