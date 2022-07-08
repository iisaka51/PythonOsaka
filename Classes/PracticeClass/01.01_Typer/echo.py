import typer

def cmd():
    typer.echo("This message oputput to stdout.")
    typer.echo("This message oputput to stderr.", err=True)

if __name__ == '__main__':
    cmd()
