import parsl
from parsl.app.app import bash_app
# from parsl.configs.local_threads import config

config = parsl.load()

@bash_app
def echo_hello(stdout='echo-hello.stdout', stderr='echo-hello.stderr'):
    return 'echo "Hello World!"'

app = echo_hello()
c = app.result()

with open('echo-hello.stdout', 'r') as f:
     print(f.read())

print(f'ExitCode: {c}')
