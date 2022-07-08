import pandas as pd

df = pd.read_csv('TSLA.csv', parse_dates=["Date"])

format_dict = {
    "Date": "{:%d/%m/%y}",
    "Open": "${:.2f}",
    "High": "${:.2f}",
    "Low": "${:.2f}",
    "Close": "${:.2f}",
    "Ajd Close": "${:.2f}",
    "Volume": "{:,}",
}

df.style.format(format_dict)
