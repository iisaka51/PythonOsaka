import click
from datetime import date

def days_delta(date):
    delta = date.today() - date
    click.echo(f"Days os life: {delta} ")

if __name__ == '__main__':
    @click.command()
    @click.option('-D', '--date', type=click.DateTime(formats=["%Y/%m/%d"]),
                  default="1962/01/13", required=False,
                  help='Your birthday')
    def cli(date):
        days_delta(date)

    cli()
