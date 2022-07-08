import typer

app = typer.Typer()

@app.command()
def hello(count: int = typer.Option(1, '-C', '--count',
                                    help='Number of greetings.'),
           name: str = typer.Option(..., prompt='Your Name',
                                    help='The person to greet.'),
         ):
    """COUNTで与えた回数だけHelloする"""
    for x in range(count):
        typer.echo(f'Hello {name}')

if __name__ == '__main__':
    app()
