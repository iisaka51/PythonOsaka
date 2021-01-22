import click
import click_utils

@click.command()
@click.option('--loglevel', type=click_utils.LogLevelChoice())
def cli(loglevel):
    click.echo(loglevel)

if __name__ == '__main__':
    cli()
