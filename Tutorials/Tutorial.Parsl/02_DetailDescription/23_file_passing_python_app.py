import os
import parsl
from parsl.app.app import python_app
from parsl.data_provider.files import File

# from parsl.configs.local_threads import config
from htex_config import htex_config as config

parsl.clear()
conf = parsl.load(config)

# 入力ファイルを作成
cwd = os.getcwd()
c = open(os.path.join(cwd, 'in.txt'), 'w').write('Hello World!\n')

# Parslの Fileオブジェクトを作成
infile = File(os.path.join(cwd, 'in.txt'),)
outfile = File(os.path.join(cwd, 'out.txt'),)

@python_app
def echo(inputs=[], outputs=[]):
    with open(inputs[0], 'r') as in_file, open(outputs[0], 'w') as out_file:
        out_file.write(in_file.readline())

app = echo(inputs=[infile], outputs=[outfile])
app.result()
