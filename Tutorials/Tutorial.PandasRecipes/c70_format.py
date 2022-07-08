import pandas as pd

df = pd.read_csv('TSLA.csv', parse_dates=['Date'])

# df
# pd.set_option('display.float_format', lambda x: '%.3f' % x)
# df
# pd.options.display.float_format = '{:,.0f}'.format
# df
