import csv

ACTIONS = dict()

def register(func):
    ACTIONS[func.__name__] = func
    return func

@register
def greeting_english(name):
    return f"Hello {name}"

@register
def greeting_french(name):
    return f"Bonjour {name}"

def greeting(name):
    greeter, greeter_func = list(ACTIONS.items())[len(name)%2]
    return(greeter_func(name))

if __name__ == '__main__':
    import click
    @click.command()
    @click.option('--namefile', '-f',  type=click.File('r'),
                  help='path to namefile')
    @click.argument('name', type=str, nargs=-1)
    def cmd(**kwargs):
        for name in kwargs['name']:
            print(greeting(name))
        names = kwargs['namefile'].readlines()
        for name in names:
            print(greeting(name[:-1]))

    cmd()
