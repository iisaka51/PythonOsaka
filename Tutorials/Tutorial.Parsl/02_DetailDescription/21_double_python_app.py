import parsl
from parsl.app.app import python_app

conf = parsl.load()

@python_app
def double(x):
    return x * 2
 
app = double(42)
print(app.result())
