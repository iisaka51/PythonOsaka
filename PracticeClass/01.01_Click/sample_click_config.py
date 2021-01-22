import click
import click_config


class config(object):
    class mysql(object):
        host = 'localhost'

@click.command()
@click_config.wrap(module=config, sections=('mysql',))
def main():
    print(f'mysql host: {config.mysql.host}')
    print(f'mysql host: {config.mysql.dbname}')


if __name__ == '__main__':
    main()
