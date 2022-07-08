import gspread_dataframe as gd
import gspread_formatting as gf
from gspread_utils import GSpread

_TICKER = 'GOOGL'
_START = 'DATE(2020,2,24)'
_END = 'DATE(2020,2,29)'

ws = GSpread('PythonOsaka_tempfile').worksheet
_ = ws.clear()
date_formats = gf.cellFormat(
                   numberFormat=gf.numberFormat(
                               type='DATE',
                               pattern='YYYY/MM/DD hh:mm'))
_ = gf.set_column_width(ws, 'B', 120)
_ = gf.format_cell_range(ws, 'B', date_formats)
cells = ws.range('B2:B6')
_ = ws.update_cells(cells, value_input_option='USER_ENTERED')

formula = (
    f'=GOOGLEFINANCE("{_TICKER}","price"'
    f',{_START},{_END})'
    )
_ = ws.update('B1', formula, raw=False)

all_rows = ws.get_all_values()
columns = all_rows.pop(0)
max_rows = len(all_rows)

df = gd.get_as_dataframe(ws,
              dtype={0: str, 1:float},
              nrows=max_rows, usecols=[1,2],
              parse_dates=['Date'],
              evaluate_formulas=True)
