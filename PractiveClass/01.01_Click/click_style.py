import click

@click.command()
def cmd():
    click.echo(click.style("Hello 1st.", fg='green', bg='red', reset=False))
    click.echo(click.style("Hello 2nd."))

if __name__ == '__main__':
    cmd()
