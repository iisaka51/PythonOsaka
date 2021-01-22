import typer
from typing import Tuple

def cmd(position: Tuple[int, int]  = typer.Option(..., '-P',  help="Geometory: x y")):
    typer.echo( position )

if __name__ == '__main__':
    typer.run(cmd)
