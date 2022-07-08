import schedule
import time

def job():
    print('Hello')

schedule.every(5).seconds.do(job)

while 1:
    n = schedule.idle_seconds()
    if n is None:
        # no more jobs
        break
    elif n > 0:
        # sleep exactly the right amount of time
        time.sleep(n)
    schedule.run_pending()

