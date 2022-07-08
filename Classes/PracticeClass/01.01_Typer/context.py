import typer

app = typer.Typer()

@app.command(
    context_settings={'allow_extra_args': True, 'ignore_unknown_options': True}
)
def main(version: bool = typer.Option(False, '--version'),
         unkown_args: typer.Context = typer.Option(None)
):
    typer.echo(f'Got known arg version: {version}')
    for unknown_arg in unkown_args.args:
        typer.echo(f'Got unknown arg: {unknown_arg}')

if __name__ == "__main__":
    app()
