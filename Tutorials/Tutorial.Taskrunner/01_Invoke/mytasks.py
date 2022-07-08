from invoke import task

@task
def show_platform(c):
    uname = c.run("uname -s").stdout.strip()
    if uname == 'Darwin':
        print("You paid the Apple tax!")
    elif uname == 'Linux':
        print("Year of Linux on the desktop!")
