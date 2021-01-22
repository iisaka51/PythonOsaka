import click
from click_params import DOMAIN

@click.command()
@click.option('-d', '--domain', type=DOMAIN)
def cmd(domain):
    click.echo(f'Your domain is {domain}')

if __name__ == '__main__':
    cmd()
