import sched
import time

scheduler = sched.scheduler(time.time, time.sleep)

def long_event(name):
    print(f' BEGIN EVENT: {time.time()} {name}')
    time.sleep(2)
    print(f'FINISH EVENT: {time.time()} {name}')

print(f'START: {time.time()}')
ev1 = scheduler.enter(2, 1, long_event, ('first',))
ev2 = scheduler.enter(3, 1, long_event, ('second',))
scheduler.run()
print(f'  END: {time.time()}')
