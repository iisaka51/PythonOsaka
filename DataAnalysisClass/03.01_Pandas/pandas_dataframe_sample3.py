import pandas as pd
history_data = {
    'Date':['2015-01-05', '2015-01-06', '2015-01-07', '2015-01-08'],
    'Open':['7565.0', '7322.0', '7256.0', '7500.0'],
    'Close':[ '7507.0', '7300.0', '7407.0', '7554.0'],
}

history_df = pd.DataFrame(history_data)
