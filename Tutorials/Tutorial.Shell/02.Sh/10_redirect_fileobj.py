import sh

with open("/tmp/current_time.txt", "a") as fp:
    sh.date(_out=fp)
