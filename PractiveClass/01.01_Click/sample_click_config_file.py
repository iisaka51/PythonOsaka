import click
import click_config_file

@click.command()
@click.option('--name', default='World', help='Who to greet.')
@click_config_file.configuration_option(
              cmd_name='click_demo',
              config_file_name='./myconfig.ini')
def hello(name):
    click.echo('Hello {}!'.format(name))

if __name__ == '__main__':
    hello()
