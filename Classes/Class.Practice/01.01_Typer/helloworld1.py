import typer

def hello_world():
    typer.echo('Hello World')

if __name__ == "__main__":
    typer.run(hello_world)
