from dataprep.datasets import load_dataset
from dataprep.clean import clean_df

df = load_dataset("titanic")
inferred_dtypes, cleaned_df = clean_df(df)
