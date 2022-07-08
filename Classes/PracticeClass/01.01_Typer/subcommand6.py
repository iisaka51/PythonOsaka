import os
import typer

__MYPROG__ = os.path.basename(__file__)
__VERSION__ = '1.0'

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

@app.callback(invoke_without_command=True)
def print_version(ctx: typer.Context,
                  version: bool = typer.Option(False, '--version')):
    if version:
        typer.echo(f'{__MYPROG__} - Version: {__VERSION__}')
        raise typer.Exit()
    if ctx.invoked_subcommand is None:
        typer.echo('This is main command')

if __name__ == "__main__":
    app()
