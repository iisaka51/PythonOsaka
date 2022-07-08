from typing import List
import typer

def copy(src: List[str] = typer.Argument(...),
         dst: str = typer.Argument(...)
):
    """Move file SRC to DST."""
    for filename in src:
        typer.echo(f'move {filename} to folder {dst}')

if __name__ == '__main__':
    typer.run(copy)
