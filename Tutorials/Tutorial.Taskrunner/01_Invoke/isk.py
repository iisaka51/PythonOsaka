from hello import hello as _hello
from hello import goodbye as _goodbye
from invoke import task

@task(iterable=['name'])
def hello(c, *name):
    "Say Hello to someone."
    print(_hello(*name))

@task()
def goodbye(c, name="World"):
    "Say Goodbye to someone."
    print(_goodbye(name))


