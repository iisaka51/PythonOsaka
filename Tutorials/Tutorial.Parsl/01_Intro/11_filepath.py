import parsl
from parsl.app.app import python_app, bash_app
from parsl.data_provider.files import File

config = parsl.load()

# ファイルの内容を別のファイルにコピーするアプリ
@bash_app
def copy(inputs=[], outputs=[]):
     cmdline = f'cat {inputs[0]} &> {outputs[0]}'
     return cmdline

# テストファイルの作成
cwd = os.getcwd()
c = open(os.path.join(cwd, 'cat-in.txt'), 'w').write('Hello World!\n')

# Parslの Fileオブジェクトを作成
parsl_infile = File(os.path.join(cwd, 'cat-in.txt'),)
parsl_outfile = File(os.path.join(cwd, 'cat-out.txt'),)

# copy アプリへ Parsl の File オブジェクトを渡して呼び出す
copy_future = copy(inputs=[parsl_infile], outputs=[parsl_outfile])

# 結果を読み出す
with open(copy_future.outputs[0].result(), 'r') as f:
     print(f.read())
