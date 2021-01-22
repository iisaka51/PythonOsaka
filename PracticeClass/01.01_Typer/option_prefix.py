import typer

def cmd(writable: bool = typer.Option(False, '+w/-w')):
    typer.echo( f'writable: {writable}' )

if __name__ == '__main__':
    typer.run(cmd)
