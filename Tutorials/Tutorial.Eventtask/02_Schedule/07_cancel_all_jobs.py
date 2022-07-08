import schedule

def greet(name):
    print('Hello {}'.format(name))

schedule.every().second.do(greet)

schedule.clear()
