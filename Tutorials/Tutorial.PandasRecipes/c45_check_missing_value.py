import pandas as pd

def missing_rate(df):
    missing = [
        (df.columns[idx], perc)
        for idx, perc in enumerate(df.isna().mean() * 100)
        if perc > 0
    ]

    if len(missing) == 0:
        return "no missing values"

    missing.sort(key=lambda x: x[1], reverse=True)

    print(f"Total of {len(missing)} variables with missing values\n")
    for label, pct in missing:
        print(str.ljust(f"{label:<20} => {round(pct, 3)}%", 1))

df = pd.read_csv('titanic.csv')
missing_rate(df)
