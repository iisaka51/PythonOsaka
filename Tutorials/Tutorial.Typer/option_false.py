import typer

def main(in_prodaction: bool = typer.Option(True, "/--demo", "/-d")):
    if in_prodaction:
        typer.echo("Running in production")
    else:
        typer.echo("Running demo")

if __name__ == "__main__":
    typer.run(main)
