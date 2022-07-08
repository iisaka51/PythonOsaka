import parsl
from parsl.app.app import python_app
from parsl.configs.local_threads import config

conf = parsl.load()

@python_app
def hello_python():
    return 'Hello world'

app = hello_python()
print(app.result())
