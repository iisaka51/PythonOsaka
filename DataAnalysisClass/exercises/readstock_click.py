from pandas_datareader import data as pdr
import pandas as pd

def readstock(ticker, start, end):
    return  pdr.get_data_yahoo('MSFT', start, end)

def writecsv(stock, csvfile):
    stock.to_csv('MSFT.csv')

if __name__ == '__main__':
    import pendulum
    import click

    start_date=str(pendulum.parse('2015-01-01',exact=True))
    end_date=str(pendulum.today().format('YYYY-MM-DD'))

    @click.command()
    @click.option('-S', '--start',
               type=click.DateTime(formats=["%Y-%m-%d"]),
               default=start_date,
               help='Start date. default: 2015-01-01')
    @click.option('-E', '--end',
               type=click.DateTime(formats=["%Y-%m-%d"]),
               default=end_date,
               help="End date default: today's date")
    @click.option('--debug', is_flag=True, default=False, hidden=True)
    @click.argument('ticker', nargs=1, required=True)
    @click.argument('csvfile', nargs=1, default=None, required=False)
    def cli(ticker, start, end, debug, csvfile):
        if debug:
            print(f'{ticker}  {start}, {end}, {csvfile}')
            exit(0)

        readstock(ticker, start, end)
        writecsv(csvfile)

    cli()
