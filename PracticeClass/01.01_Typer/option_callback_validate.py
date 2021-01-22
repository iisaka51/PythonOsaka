import typer

def name_callback(value: str):
    if value != "Freddie":
        raise typer.BadParameter("Only Freddie is allowed")
    return value

def main(name: str = typer.Option(..., callback=name_callback)):
    typer.echo(f"Hello {name}")

if __name__ == "__main__":
    typer.run(main)
