from datetime import datetime
import typer

def main(start: datetime = typer.Option(...),
         end: datetime = typer.Argument(
                               f'{datetime.today():%Y-%m-%d}'),
):
    typer.echo(f'start: {start}')
    typer.echo(f'  end: {end}')


if __name__ == "__main__":
    typer.run(main)
