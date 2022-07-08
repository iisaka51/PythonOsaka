import parsl
import os
from parsl.app.app import python_app, bash_app
from parsl.data_provider.files import File

config = parsl.load()

# 入力で与えられた message を出力ファイルに出力するアプリ
@bash_app
def slowecho(message, outputs=[]):
    cmdline = f'sleep 5; echo {message} &> {outputs[0]}'
    return cmdline

# 出力ファイルを指定してslowechoを呼び出す
outfile = File(os.path.join(os.getcwd(), 'hello-world.txt'))
hello = slowecho('Hello World!', outputs=[outfile])

# AppFutureのoutputs プロパティーは、DataFuturesのリストです。
print(hello.outputs)

# AppFutures が終了したかチェック
print(f'Done: {hello.done()}')

# 出力されたDataFutureの内容を、AppFuture の終了時に出力する
with open(hello.outputs[0].result(), 'r') as f:
     print(f.read())

# ここでDataFutures とAppFuture が終了したかを確認
print(hello.outputs)
print(f'Done: {hello.done()}')
