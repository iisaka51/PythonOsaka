import schedule

def some_task():
    print('Hello world')

job = schedule.every().day.at('22:30').do(some_task)
schedule.cancel_job(job)
