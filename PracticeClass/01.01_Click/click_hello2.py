import click

@click.command()
@click.option('-C', '--count', default=1, type=int, help='Number of greetings.')
@click.option('--name', prompt='Your name', type=str, help='The person to greet.')
def hello(**kwargs):
    print(kwargs)

hello()
