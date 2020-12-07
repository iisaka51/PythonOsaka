import typer
from datetime import datetime

def days_delta(date):
    delta = date.today() - date
    typer.echo(f"Days os life: {delta} ")

if __name__ == '__main__':
    def cli(date: datetime = typer.Option('1962/01/13', formats=["%Y/%m/%d"],
                  help='Your birthday')
        ):
        days_delta(date)

    typer.run(cli)
