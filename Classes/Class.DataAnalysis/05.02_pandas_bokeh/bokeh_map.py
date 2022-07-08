import pandas as pd
import pandas_bokeh

githuburl = 'https://raw.githubusercontent.com/'
baseurl = r'PatrikHlobil/Pandas-Bokeh/master/docs/Testdata/populated%20places/'
url = githuburl + baseurl + 'populated_places.csv'
df_map = pd.read_csv(url)

df_map["size"] = df_map["pop_max"] / 1000000
df_map.plot_bokeh.map(
    x="longitude",
    y="latitude",
    hovertool_string="""<h2> @{name} </h2>

                        <h3> Population: @{pop_max} </h3>""",
    tile_provider="STAMEN_TERRAIN_RETINA",
    size="size",
    figsize=(900, 600),
    title="World cities with more than 1.000.000 inhabitants")
