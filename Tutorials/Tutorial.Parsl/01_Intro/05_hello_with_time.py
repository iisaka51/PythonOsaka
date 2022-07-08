import parsl
from parsl.app.app import python_app
# from parsl.configs.local_threads import config

config = parsl.load()

@python_app
def hello_python():
    import datetime
    return f'Hello world: {datetime.datetime.now()}'

app = hello_python()
print(app.result())
