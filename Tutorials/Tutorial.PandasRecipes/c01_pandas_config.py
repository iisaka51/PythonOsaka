import pandas as pd

config = { 'display.max_rows': 100,
           'display.max_columns': 80,
           'display.max_colwidth': 20 }

print({x: pd.get_option(x) for x in config.keys()})      # 取得
_ = [pd.set_option(k,v) for k, v in config.items()]      # 変更
_ = [pd.reset_option(x) for x in config.keys()]          # リセっっと
