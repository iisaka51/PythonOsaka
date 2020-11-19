import click

@click.command()
@click.argument('src', nargs=-1, required=True)
@click.argument('dst', nargs=1)
def copy(src, dst):
    """Move file SRC to DST."""
    for filename in src:
        click.echo(f'move {filename} to folder {dst}')

if __name__ == '__main__':
    copy()

