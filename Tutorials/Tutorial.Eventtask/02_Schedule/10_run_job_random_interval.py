def my_job():
    print('Foo')

# Run every 5 to 10 seconds.
schedule.every(5).to(10).seconds.do(my_job)
