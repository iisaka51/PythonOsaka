import dask.bag as db

def pi(num_points):
    from random import random

    inside = 0
    for i in range(num_points):
        x, y = random(), random()
        if x**2 + y**2 < 1:
            inside += 1

    return (inside*4 / num_points)

def do_dask(nparts):
    seq = [100**6 for i in range(100)]
    bagseq = db.from_sequence(seq, npartitions = nparts)
    t1 = time.ime()
    c = bagseq.map(lambda x: do_pi(x)).mean()
    x = c.compute()
    t2 = time.time()
    total_time = t2 - t1
    print(f'total time={total_time}')
    return total_time

blocklist = [1, 2, 4, 5, 10, 20, 100]
vals = []
for i in blocklist:
    vals.append(do_dask(i))
