import os
import parsl
from parsl.providers import LocalProvider
from parsl.channels import LocalChannel
from parsl.config import Config
from parsl.executors import HighThroughputExecutor
from parsl.app.app import python_app, bash_app
from parsl.data_provider.files import File

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

@python_app
def pi(num_points):
    from random import random

    inside = 0
    for i in range(num_points):
        x, y = random(), random()
        if x**2 + y**2 < 1:
            inside += 1

    return (inside*4 / num_points)

def do_parsl(blocks):
    t1 = time.ime()
    vals = 0
    for j in range(int(100/blocks)):
        clist = []
        for i in range(blocks):
            clist.append(pi(10**6))
        for i in range(blocks):
            vals += clist[i].result()
    t2 = time.time()
    total_time = t2 - t1
    print(f'total time={total_time}')
    return total_time

blocklist = [1, 2, 4, 5, 10, 20, 100]
parsl_vals = []
for i in blocklist:
    parsl_vals.append(dp_pars(i))
