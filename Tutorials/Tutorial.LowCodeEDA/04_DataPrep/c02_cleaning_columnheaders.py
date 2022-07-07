from dataprep.datasets import load_dataset
from dataprep.clean import clean_headers

df = load_dataset("titanic")

df.columns
clean_headers(df, case = 'const').columns
clean_headers(df, case = 'camel').columns

