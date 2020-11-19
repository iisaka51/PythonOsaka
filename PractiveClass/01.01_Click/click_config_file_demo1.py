import click
import click_config_file

@click.command('hello')
@click.option('--name', default='World', help='Who to greet.')
@click_config_file.configuration_option()
def hello(name):
    click.echo(f'Hello {name}!')

if __name__ == '__main__':
    hello()
