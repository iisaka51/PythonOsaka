from datetime import date

def days_delta(start_date, end_date):
    delta = end_date - start_date
    click.echo(f"Days os deleta: {delta} ")

if __name__ == '__main__':
    import click
    @click.command()
    @click.option('-S', '--start_date', type=click.DateTime(formats=["%Y-%m-%d"]),
                  default="1962-01-13", required=False,
                  help='Start date')
    @click.option('-E', '--end_date', type=click.DateTime(formats=["%Y-%m-%d"]),
                  default=str(date.today()), required=False,
                  help='End date')
    def cli(start_date, end_date):
        days_delta(start_date, end_date)

    cli()
