import schedule
import time

def job_that_executes_once():
    # Do some work that only needs to happen once...
    return schedule.CancelJob

schedule.every().day.at('22:30').do(job_that_executes_once)

while True:
    schedule.run_pending()
    time.sleep(1)
