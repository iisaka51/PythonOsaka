from pandas_datareader import data as pdr
import pandas as pd

class StockCSV:
    def __init__(self):
        pass
    def readcsv(self, csvfile):
        self.stock = pd.read_csv(csvfile)
        return self.stock
    def writecsv(self, stock=None, csvfile=None):
        if stock == None:
            stock = self.stock
        if csvfile != None:
            df.to_csv(csvfile)
    def readstock(self, ticker, start, end):
        self.stock = pdr.get_data_yahoo(ticker, start, end)
        return self.stock


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

        stock = StockCSV()
        stock.readstock(ticker, start, end)
        stock.writecsv(csvfile)

    cli()
