import typer

def complete_name():
    return ["Jack", "David", "Freddie"]

def main(
    name: str = typer.Option("World",
                      autocompletion=complete_name,
                      help="The name to say hi to."
    )
):
    typer.echo(f"Hello {name}")

if __name__ == "__main__":
    typer.run(main)
