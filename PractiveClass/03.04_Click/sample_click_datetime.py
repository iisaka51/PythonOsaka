from datetime import date
import click

@click.command()
@click.option('-S', '--start', type=click.DateTime(formats=["%Y-%m-%d"]),
              default=str(date.today()),
              help='Start date')
@click.option('-E', '--end', type=click.DateTime(formats=["%Y-%m-%d"]),
              default=str(date.today()),
              help='End date')
def cmd(start, end):
    click.echo(f"Start: {start}, End: {end} ")
    date_difference = end - start
    click.echo(f"Date Difference: {date_difference} ")


if __name__ == '__main__':
    cmd()
