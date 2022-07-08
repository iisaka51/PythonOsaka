import schedule
from datetime import datetime, timedelta, time

def job():
    print('Boo')

# run job until a 18:30 today
schedule.every(1).hours.until("18:30").do(job)

# run job until a 2030-01-01 18:33 today
schedule.every(1).hours.until("2030-01-01 18:33").do(job)

# Schedule a job to run for the next 8 hours
schedule.every(1).hours.until(timedelta(hours=8)).do(job)

# Run my_job until today 11:33:42
schedule.every(1).hours.until(time(11, 33, 42)).do(job)

# run job until a specific datetime
schedule.every(1).hours.until(datetime(2020, 5, 17, 11, 36, 20)).do(job)
