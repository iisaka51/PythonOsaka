import os
import parsl
from parsl.providers import LocalProvider
from parsl.channels import LocalChannel
from parsl.config import Config
from parsl.executors import HighThroughputExecutor
from parsl.app.app import python_app, bash_app
from parsl.data_provider.files import File

# See Also: 22_parallel_dataflow.py

local_htex = Config(
    executors=[
        HighThroughputExecutor(
            label="htex_Local",
            worker_debug=True,
            cores_per_worker=1,
            provider=LocalProvider(
                channel=LocalChannel(),
                init_blocks=1,
                max_blocks=1,
            ),
        )
    ],
    strategy=None,
)

parsl.clear()
parsl.load(local_htex)


# 0〜32,767の範囲の疑似乱数を生成
@bash_app
def generate(outputs=[]):
    cmdline = f"echo $(( RANDOM )) &> {outputs[0]}"
    return cmdline

# 複数の入力ファイルを１つのファイルに連結するアプリ
@bash_app
def concat(inputs=[], outputs=[]):
    infiles = " ".join([i.filepath for i in inputs])
    cmdline  =  f'cat {infiles} > {outputs[0]}'
    return cmdline

# リストで与えた入力ファイルの内容（数値）を合計するアプリ
@python_app
def total(inputs=[]):
    total = 0
    with open(inputs[0], 'r') as f:
        for l in f:
            total += int(l)
    return total

# 5つの乱数ファイルを並列で生成する
output_files = []
for i in range (5):
     outfile = File(os.path.join(os.getcwd(), f'random-{i}.txt'))
     output_files.append(generate(outputs=[outfile]))

# 5つの乱数ファイルを１つのファイルに連結する
infiles = [i.outputs[0] for i in output_files]
outfile= File(os.path.join(os.getcwd(), 'cmbined.txt'))
cc = concat(inputs=infiles, outputs=[outfile])

# 乱数の合計を計算
total = total(inputs=[cc.outputs[0]])
print (total.result())
