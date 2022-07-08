import typer

app = typer.Typer()

@app.command("hello")
def hello_world():
    typer.echo('Hello World')

if __name__ == "__main__":
    app()
