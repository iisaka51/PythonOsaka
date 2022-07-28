import sweetviz as sv
import pandas as pd

train_df = pd.read_csv('http://cooltiming.com/SV/train.csv')

report = sv.compare_intra([train_df, "Titanic"],
                          train_df["Sex"] == "male",
                          ["Male", "Female"])

report.show_html(filepath='Titanic_Comp_Intra.html',
                 layout='vertical', scale=1.0)
# or
# report.show_notebook()
