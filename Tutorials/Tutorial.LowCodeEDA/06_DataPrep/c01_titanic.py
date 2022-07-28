from dataprep.datasets import load_dataset
from dataprep.eda import create_report

df = load_dataset("titanic")
df.head()
df.to_csv('titanic.csv')
# create_report(df).show_browser()
#
