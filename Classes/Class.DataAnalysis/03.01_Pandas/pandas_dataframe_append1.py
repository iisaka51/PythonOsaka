import pandas as pd
history_data1 = {
    'Date':['2015-01-05', '2015-01-06', '2015-01-07', '2015-01-08'],
    'Open':['7565.0', '7322.0', '7256.0', '7500.0'],
    'Close':[ '7507.0', '7300.0', '7407.0', '7554.0'],
}
history_data2 = {
    'Date':['2015-01-09', '2015-01-10'],
    'Open':['7630.0','7440.0'],
    'Close':['7609.0','7519.0'],
}

history_df1 = pd.DataFrame(history_data1)
history_df2 = pd.DataFrame(history_data2)
