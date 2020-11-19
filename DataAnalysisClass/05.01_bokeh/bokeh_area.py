import pandas as pd
import pandas_bokeh

githuburl = 'https://raw.githubusercontent.com/'
baseurl = 'PatrikHlobil/Pandas-Bokeh/master/'
url = githuburl + baseurl + 'docs/Testdata/energy/energy.csv'

df_energy = pd.read_csv(url, parse_dates=["Year"])
df_energy.head()

df_energy.plot_bokeh.area(
    x="Year",
    stacked=True,
    location="top_left",
    colormap=["brown", "orange", "black", "grey", "blue", "green"],
    title="Worldwide energy consumption split by energy source",
    ylabel="Million tonnes oil equivalent",
    ylim=(0, 16000))
