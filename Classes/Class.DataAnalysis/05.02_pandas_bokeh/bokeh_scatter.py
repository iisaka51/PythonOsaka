import pandas as pd
import pandas_bokeh

baseurl = 'https://raw.githubusercontent.com/PatrikHlobil/Pandas-Bokeh/'
url = baseurl + 'master/docs/Testdata/iris/iris.csv'

df = pd.read_csv(url)
df = df.sample(frac=1)

#Change one value to clearly see the effect of the size keyword
df.loc[13, "sepal length (cm)"] = 15

#Make scatterplot:
p_scatter = df.plot_bokeh.scatter(
    x="petal length (cm)",
    y="sepal width (cm)",
    category="species",
    title="Iris DataSet Visualization with Size Keyword",
    size="sepal length (cm)")
