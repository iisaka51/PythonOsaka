import sched
import time
from datetime import datetime

def time_addition(a,b):
    print("\nInside Addition : ", datetime.now())
    print("Time : ", time.monotonic())
    print("Result : ", a+b)

scheduler = sched.scheduler()

print("Start Time : ", datetime.now(), "\n")

current_time = time.monotonic()
current_time_plus_5 = current_time + 5

event = scheduler.enterabs(current_time_plus_5, 1,
                           time_addition, kwargs = {"a":10, "b":20})

print("Current Time  : ", current_time)

print("\nEvent Created : ", event)
scheduler.run()

print("\nEnd   Time : ", datetime.now())
