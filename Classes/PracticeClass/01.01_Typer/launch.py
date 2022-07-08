import typer

def hello_world():
    """our first CLI with typer!
    """
    typer.echo("Opening blog post...")
    typer.launch(
        "https://pluralsight.com/tech-blog/python-cli-utilities-with-poetry-and-typer"
    )


if __name__ == "__main__":
    typer.run(hello_world)
