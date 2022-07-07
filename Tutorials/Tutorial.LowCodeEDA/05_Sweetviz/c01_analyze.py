import sweetviz as sv
import pandas as pd

train_df = pd.read_csv('http://cooltiming.com/SV/train.csv')

report = sv.analyze([train_df,'Train'],
                    target_feat='Survived')

report.show_html(filepath='Titanic_EDA.html',
                 layout='vertical', scale=1.0)
# or
# report.show_notebook()
