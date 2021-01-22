import click

@click.command()
@click.option("--uuid", type=click.UUID, required=True)
def cmd(uuid):
    click.echo(f'uuid={uuid}')

if __name__ == '__main__':
    cmd()
