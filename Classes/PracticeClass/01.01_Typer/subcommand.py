import typer

app = typer.Typer()

@app.command()
def initdb(dbname: str):
    typer.echo(f'Initialized the database {dbname}')

@app.command()
def dropdb(force: bool = typer.Option(False, '--force',
                           help='drop db anyway'),
           dbname: str = typer.Argument(...)
):
    typer.echo(f'Force Flag: {force}')
    typer.echo(f'Droped the database: {dbname}')


if __name__ == "__main__":
    app()
