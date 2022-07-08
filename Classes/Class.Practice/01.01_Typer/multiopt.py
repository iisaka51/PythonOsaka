import typer
from typing import List

def cmd(name: List[str] = typer.Option(..., '-N', '--name', help="Name...")):
    typer.echo( name )

if __name__ == '__main__':
    typer.run(cmd)
