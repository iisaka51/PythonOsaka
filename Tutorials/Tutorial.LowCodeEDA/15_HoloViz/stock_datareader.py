from datetime import datetime
import pandas as pd
import pandas_datareader as pdr

def load_data(ticker="^GSPC", start=None, end=None, filename=None):
   try:
       start = datetime.fromisoformat(start)
   except:
       start = datetime(datetime.now().year, 1, 1)
   try:
       end = datetime.fromisoformat(end)
   except:
       end = datetime.today()

   df = pdr.DataReader(ticker, 'yahoo', start, end)
   _ = filename and df.to_csv(filename)
   return df

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(description ='stock data reader')
    parser.add_argument(dest='ticker', metavar='ticker',
                        action='store', nargs=1,
                        help='ticker symbol. i.e.: SP500 is "^GSPC"')
    parser.add_argument('-F', '--filename', metavar='filename',
                        dest='filename', default=None,
                        help='save filename. default is None')
    parser.add_argument('-S', '--start', metavar='YYYY-MM-DD',
                        dest='start', action='store',
                        help='date of start. default is Jan 1st of this year')
    parser.add_argument('-E', '--end', metavar='YYYY-MM-DD',
                        dest='end', action='store',
                        help='date of end. default is today')

    args = parser.parse_args()
    load_data(args.ticker[0], args.start, args.end, args.filename)
