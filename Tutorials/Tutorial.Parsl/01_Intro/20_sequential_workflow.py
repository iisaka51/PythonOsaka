import parsl
from parsl.app.app import python_app, bash_app
from parsl.data_provider.files import File

config = parsl.load()

# 乱数を生成するアプリ
@python_app
def generate(limit):
      from random import randint
      return randint(1,limit)

# ファイルに値を書き出すアプリ
@bash_app
def save(variable, outputs=[]):
      cmdline = f'echo {variable} &> {outputs[0]}'
      return cmdline

# 1〜10の範囲で乱数を生成
random = generate(10)
print(f'Random number: {random.result()}')

# 乱数をファイルに保存
outfile = File(os.path.join(os.getcwd(), 'sequential-output.txt'))
saved = save(random, outputs=[outfile])

# 結果を出力
with open(saved.outputs[0].result(), 'r') as f:
    data = f.read()
    print(f'File contents: {data}')
