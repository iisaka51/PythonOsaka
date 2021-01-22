import click

@click.command()
@click.option('-C', '--count', default=1, type=int, help='Number of greetings.')
@click.option('--name', prompt='Your name', type=str, help='The person to greet.')
def hello(count, name):
    """COUNTで与えた回数だけHelloする"""
    for x in range(count):
        click.echo(f'Hello {name}!')

if __name__ == '__main__':
    hello()
