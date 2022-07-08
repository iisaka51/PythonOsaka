import parsl
from parsl.app.app import python_app
# from parsl.configs.local_threads import config

config = parsl.load()

@python_app
def multiply(a, b):
    return a * b

app = multiply(5, 9)
print(app.result())
