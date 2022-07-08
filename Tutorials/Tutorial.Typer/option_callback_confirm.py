import typer

def abort_if_false(ctx, param, value):
    if not value:
        typer.abort()

def cmd(yes: bool = typer.Option(...,
                          expose_value=True,
                          prompt='Are you sure you want to drop the db?',
                          callback=abort_if_fals)
):
    typer.echo('Dropped all tables!')

if __name__ == '__main__':
    cmd()
