import schedule

def hello():
    print('Hello world')

schedule.every().second.do(hello)

all_jobs = schedule.get_jobs()
