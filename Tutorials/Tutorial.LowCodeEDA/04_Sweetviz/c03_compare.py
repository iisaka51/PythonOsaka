import sweetviz as sv
import pandas as pd

train_df = pd.read_csv('http://cooltiming.com/SV/train.csv')
test_df = pd.read_csv('http://cooltiming.com/SV/test.csv')

report = sv.compare([train_df,'Train'],
                    [test_df,'Test'],
                    target_feat='Survived')

report.show_html(filepath='Titanic_Compare.html',
                 layout='vertical', scale=1.0)
# or
# report.show_notebook()
