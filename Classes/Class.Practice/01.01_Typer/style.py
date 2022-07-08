import typer

def cmd():
    typer.echo(typer.style('Hello World.',
                           fg='green', bg='red', reset=False))
    typer.echo(typer.style('Hello Again.'))

if __name__ == '__main__':
    cmd()
