import pandas as pd

df = pd.read_csv('TSLA.csv', parse_dates=["Date"])
df = df[df["Date"].dt.strftime("%Y") == "2018"]

format_dict = {
    "Date": "{:%d/%m/%y}",
    "Open": "${:.2f}",
    "High": "${:.2f}",
    "Low": "${:.2f}",
    "Close": "${:.2f}",
    "Ajd Close": "${:.2f}",
    "Volume": "{:,}",
}

(
    df.style.format(format_dict)
    .hide_index()
    .highlight_min(["Open"], color="red")
    .highlight_max(["Open"], color="green")
    .background_gradient(subset="Close", cmap="Greens")
    .bar('Volume', color='lightblue', align='zero')
    .set_caption('Tesla Stock Prices in 2018')
)
