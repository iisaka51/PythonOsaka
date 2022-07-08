import time
from timeloop import Timeloop
from datetime import timedelta

tl = Timeloop()

@tl.job(interval=timedelta(seconds=2))
def sample_job_every_2s():
    print(f'2s job current time : {time.ctime()}')

@tl.job(interval=timedelta(seconds=5))
def sample_job_every_5s():
    print(f'5s job current time : {time.ctime()}')

@tl.job(interval=timedelta(seconds=10))
def sample_job_every_10s():
    print(f'10s job current time : {time.ctime()}')

if __name__ == '__main__':
    tl.start(block=True)
