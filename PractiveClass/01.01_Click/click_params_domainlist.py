import click
from click_params import DomainListParamType

@click.command()
@click.option('-d', '--domains',
              type=DomainListParamType(' '),
              help='list of domain names separated by a white space')
def cmd(domains):
    click.echo('Your list of domain names:')
    for domain in domains:
        click.echo(f'- {domain}')

if __name__ == '__main__':
    cmd()
