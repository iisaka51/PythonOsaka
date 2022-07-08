import parsl
from parsl.app.app import python_app

config = parsl.load()

@python_app
def hello():
    import time
    time.sleep(5)
    return 'Hello World'

app = hello()

# app が終了済みかどうかをチェックする
print(f'Done: {app.done()}')

# app の結果を出力する
# 注意：この呼び出しはブロックされ、app の終了を待つ
print(f'Result: {app.result()}')

print(f'Done: {app.done()}')
