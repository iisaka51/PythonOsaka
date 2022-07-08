from datetime import datetime
import pandas as pd
history_data = {
    'Date':[
        datetime(2015,1,5),
        datetime(2015,1,6),
        datetime(2015,1,7),
        datetime(2015,1,8)
        ],
    'Open':[7565.0, 7322.0, 7256.0, 7500.0],
    'Close':[ 7507.0, 7300.0, 7407.0, 7554.0],
}

history_df = pd.DataFrame(history_data)
