import pandas as pd
history_data = {
    'Date':['2015-01-05', '2015-01-06', '2015-01-07', '2015-01-08'],
    'Open':['7565.0', '7322.0', '7256.0', '7500.0'],
    'Close':[ '7507.0', '7300.0', '7407.0', '7554.0'],
}
adjClose_data = [
    '6402.83447265625',
    '6226.2802734375',
    '6317.54296875',
    '6442.92138671875',
]

history_df = pd.DataFrame(history_data)
history_df['AdjClose'] = adjClose_data
