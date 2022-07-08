import parsl
from parsl.app.app import bash_app
from parsl.data_provider.files import File

config = parsl.load()

@bash_app
def cat(inputs=[], outputs=[]):
    infiles = " ".join([i.filepath for i in inputs])
    return f'cat {infiles} > {outputs[0]}'

cwd = os.getcwd()
concat = cat(inputs=[File(os.path.join(cwd, 'hello-0.txt')),
                     File(os.path.join(cwd, 'hello-1.txt')),
                     File(os.path.join(cwd, 'hello-2.txt'))],
             outputs=[File(os.path.join(cwd, 'all_hellos.txt'))])

# 結果ファイルを読み出す
with open(concat.outputs[0].result(), 'r') as f:
     print(f.read())
