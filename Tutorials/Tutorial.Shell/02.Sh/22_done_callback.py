import sh
from threading import Semaphore

pool = Semaphore(10)

def done(cmd, success, exit_code):
    pool.release()

def do_thing(arg):
    pool.acquire()
    return sh.sleep('20', _bg=True, _done=done)

procs = []
for arg in range(10):
    procs.append(do_thing(arg))

for p in procs:
    p.wait()
    print(f'{p.pid}')

