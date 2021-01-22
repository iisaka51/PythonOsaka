from datetime import datetime
import click

class Date(click.ParamType):
    name = 'date'

    def __init__(self, formats=None):
        self.formats = formats or [
            '%Y-%m-%d',
            '%Y-%m-%d %H:%M:%S'
        ]

    def get_metavar(self, param):
        return '[{}]'.format('|'.join(self.formats))

    def _try_to_convert_date(self, value, format):
        try:
            return datetime.strptime(value, format).date()
        except ValueError:
            return None

    def convert(self, value, param, ctx):
        for format in self.formats:
            date = self._try_to_convert_date(value, format)
            if date:
                return date

        self.fail(
            'invalid date format: {}. (choose from {})'.format(
                value, ', '.join(self.formats)))

    def __repr__(self):
        return 'Date'

@click.command()
@click.option('-S', '--start', type=Date(),
              default=str(datetime.today()),
              help='Start datetime')
@click.option('-E', '--end', type=Date(),
              default=str(datetime.today()),
              help='End datetime')
def cmd(start, end):
    date_difference = end - start
    print(f'Start: {start},   End: {end} ')
    click.echo(f"Date Difference: {date_difference} ")

if __name__ == '__main__':
     cmd()
