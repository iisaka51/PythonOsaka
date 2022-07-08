import typer

app = typer.Typer(help='Database manager')

@app.command(help='Initializing DATABASE')
def initdb(dbname: str):
    """
    Initializing database.
    """
    typer.echo(f'Initialized the database {dbname}')

@app.command("dropdb")
def delete_db(force: bool = typer.Option(False, '--force',
                           help='drop db anyway'),
           dbname: str = typer.Argument(...)
):
    """
    Drop database.
    """
    typer.echo(f'Force Flag: {force}')
    typer.echo(f'Droped the database: {dbname}')


if __name__ == "__main__":
    app()
