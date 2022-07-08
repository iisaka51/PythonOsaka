from typing import List
import typer

def copy(src: List[str] = typer.Argument(..., metavar='SOURCES'),
         dst: str = typer.Argument(..., metavar='DESTINATION')
):
    """Move file SOURCES to DESTINATION."""
    for filename in src:
        typer.echo(f'move {filename} to folder {dst}')

if __name__ == '__main__':
    typer.run(copy)
