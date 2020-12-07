import typer
from datetime import datetime

def days_delta(start_date, end_date):
    delta = end_date - start_date
    typer.echo(f"Days os deleta: {delta} ")

if __name__ == '__main__':
    def cli(staert: datetime = typer.Option('1962-01-13',
                                     formats=["%Y-%m-%d"],
                                     help='Start date')
               end: datetime = typer.Option( str(date.today()),
                                     formats=["%Y-%m-%d"],
                                      help='Start date')
        days_delta(start_date, end_date)

    typer.run(cli)
