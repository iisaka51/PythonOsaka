import parsl
import os
from parsl.app.app import python_app, bash_app

# すべてのログを標準出力へ送出
parsl.set_stream_logger()

conf = parsl.load()

@python_app
def hello_python (message):
    return f'Hello {message}'

@bash_app
def hello_bash(message, stdout='hello-stdout'):
    return f'echo "Hello {message}"'

# Pythonアプリを起動
p = hello_python('World (Python)')

# Bashスクリプトを実行
b = hello_bash('World (Bash)')
c = b.result()

# 結果を表示する
print(p.result())
with open('hello-stdout', 'r') as f:
    print(f.read())

print(f'bash exit code: {c}')
