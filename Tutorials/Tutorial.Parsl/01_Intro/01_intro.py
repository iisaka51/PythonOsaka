import parsl
import os
from parsl.app.app import python_app, bash_app
# from parsl.configs.local_threads import config

conf = parsl.load()

@python_app
def hello_python (message):
    return f'Hello {message}'

@bash_app
def hello_bash(message, stdout='hello-stdout'):
    return f'echo "Hello {message}"'

# Pythonアプリを起動し、結果を表示する
p = hello_python('World (Python)')
print(p.result())

# Bashスクリプトを実行し、結果を表示する
b = hello_bash('World (Bash)')
b.result()

with open('hello-stdout', 'r') as f:
    print(f.read())
