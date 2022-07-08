import typer

app = typer.Typer(help='Database manager')
state = {'verbose': False }

@app.command(help='Initializing DATABASE')
def initdb(dbname: str):
    """
    Initializing database.
    """
    if state["verbose"]:
       typer.echo("running initializing database")
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
    if state["verbose"]:
       typer.echo("running drop database")
    typer.echo(f'Droped the database: {dbname}')

@app.callback()
def main(verbose: bool = typer.Option(False, '--verbose')):
    typer.echo("Running a command")
    if verbose:
        typer.echo("Will write verbose output")
        state["verbose"] = True

if __name__ == "__main__":
    app()
