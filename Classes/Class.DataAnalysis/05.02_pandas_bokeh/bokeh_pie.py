import pandas as pd
import pandas_bokeh

githuburl = 'https://raw.githubusercontent.com/'
baseurl = 'PatrikHlobil/Pandas-Bokeh/master/'
url = githuburl + baseurl + 'docs/Testdata/Bundestagswahl/Bundestagswahl.csv'

df_pie = pd.read_csv(url)

df_pie.plot_bokeh.pie(
    x="Partei",
    y="2017",
    colormap=["blue", "red", "yellow", "green", "purple", "orange", "grey"],
    title="Results of German Bundestag Election 2017",
    )
