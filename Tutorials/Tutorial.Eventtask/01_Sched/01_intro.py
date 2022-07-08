import sched
import time

scheduler = sched.scheduler(time.time, time.sleep)
def print_time(arg='default'):
    print(f'Event: {time.time()} {arg}')

def do_something():
    print(f'START: {time.time()}')
    ev1 = scheduler.enter(10, 1, print_time)
    ev2 = scheduler.enter(5, 2, print_time, argument=('positional',))
    ev3 = scheduler.enter(5, 1, print_time, kwargs={'arg': 'keyword'})
    scheduler.run()
    print(f'END: {time.time()}')
    return (ev1, ev2, ev3)

ev = do_something()

# print(ev[0])
# print(ev[1])
# print(ev[2])
