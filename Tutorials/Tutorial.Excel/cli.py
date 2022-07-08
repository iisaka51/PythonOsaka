# standard libs
from pathlib import Path

# external libs
from cmdkit.app import Application, exit_status
from cmdkit.cli import Interface, ArgumentError
from cmdkit.config import Configuration

# internal libs
from config import workdir, homedir, SpliterConfig

myconf = Configuration.from_local(
                 default = SpliterConfig().__dict__,
                 env = False, prefix='',
                 user = str(homedir / '.excel_spliter.yml'),
                 local = str(workdir / 'excel_spliter.yml'))

APP_NAME='excel_spliter'
APP_DESCRIPTION=f"""\
{APP_NAME} - Spliter columns data from target column in EXCEL Sheet.
"""

APP_USAGE=f"""
{APP_DESCRIPTION}

Usage: {APP_NAME} [OPTIONS] <infile> [outfile]
"""

APP_HELP=f"""
{APP_USAGE}
Arguments:
 infile              The path to input file. REQUIRE.
 outfile             The path to output file. OPTIONAL.
                     default is change suffix ".xslx" to ".conv.xslx"


Options:
    -w, --worksheet   The name of processing worksheet.
    -r, --min_row     The number of Maximum row
                      default is "{myconf.MIN_ROW}"
    -R, --max_row     The number of Maximum row
                      default is "{myconf.MAX_ROW}"
    -c, --column      The name of processing column.
                      default is {myconf.COLUMN_RANGE}
    -d, --delimitor   the field delimiter character.
                      default is "{myconf.DELIMITOR}"
    -h, --help        show this message and exit.
"""

class MyApp(Application):

    ALLOW_NOARGS: bool = False
    interface = Interface(APP_NAME, APP_USAGE, APP_HELP)

    infile: Path
    outfile: Path

    min_row: int = myconf.MIN_ROW
    max_row: int = myconf.MAX_ROW

    interface.add_argument('infile', type=Path, nargs='1')
    interface.add_argument('outfile', type=Path, nargs='?',
                           default=( f'{Path(path).stem}'
                                      '.conv'
                                     f'{Path(path).suffix}'))

    interface.add_argument('-w', '--worksheet', type=str,
                           default=worksheet )
    interface.add_argument('-s', '--skip_raws', type=int,
                           default=skip_raws )
    interface.add_argument('-c', '--column', type=str,
                           default=column )
    interface.add_argument('-d', '--delimitor', type=str,
                           default=delimitor )

    def run(self):
        print(f'infile: {self.infile}')
        print(f'outfile: {self.outfile}')
        print(f'worksheet: {self.worksheet}')
        print(f'min_row: {self.min_row}')
        print(f'max_row: {self.max_row}')
        print(f'column: {self.column}')

        wb = openpyxl.load_workbook(infile)
        ws = wb["Sheet1"]

        for row in ws.iter_rows( min_row=self.skip_raws,
                                 max_row
                             max_col=3, max_row=2):
            for cell in row:
                print(cell)

if __name__ == '__main__':
    import sys
    try:
        MyApp.main(sys.argv[1:])
    except NotADirectoryError:
        print(APP_USAGE)
        print(f"<path> must be directory.")
        sys.exit(1)
