import typer

def cmd(debug: bool = typer.Option(False, help='DEBUG mode', hidden=True),
        force: bool = typer.Option(False, '--force', help='Force option')
):
    typer.echo( f'debug: {debug}')
    typer.echo( f'force: {force}')

if __name__ == '__main__':
    typer.run(cmd)
