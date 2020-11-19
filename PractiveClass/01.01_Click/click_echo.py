import click

@click.command()
def cmd():
    click.echo("Command was Done.")

if __name__ == '__main__':
    cmd()
