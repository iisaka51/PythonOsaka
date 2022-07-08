import sched
import time

scheduler = sched.scheduler(time.time, time.sleep)

def print_event(name):
    print(f'EVENT: {time.time()} {name}')

now = time.time()
print(f'START: {now}')
ev = scheduler.enterabs(now+2, 2, print_event, ('first',))
ev = scheduler.enterabs(now+2, 1, print_event, ('second',))
scheduler.run()
print(f'  END: {time.time()}')
