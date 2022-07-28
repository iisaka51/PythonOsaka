import sweetviz as sv
import pandas as pd

train_df = pd.read_csv('http://cooltiming.com/SV/train.csv')

sv.config_parser.read('config.ini')
report = sv.analyze([train_df,'Train'],
                    target_feat='Survived')

# or
# report.show_notebook()
