import pandas as pd
import pandas_bokeh


baseurl = 'https://raw.githubusercontent.com/PatrikHlobil/Pandas-Bokeh/'
url = baseurl + 'master/docs/Testdata/iris/iris.csv'

df = pd.read_csv(url)
df = df.sample(frac=1)

# Create Bokeh-Table with DataFrame:
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.models import ColumnDataSource

data_table = DataTable(
    columns=[TableColumn(field=Ci, title=Ci) for Ci in df.columns],
    source=ColumnDataSource(df),
    height=300,
)

# Create Scatterplot:
p_scatter = df.plot_bokeh.scatter(
    x="petal length (cm)",
    y="sepal width (cm)",
    category="species",
    title="Iris DataSet Visualization",
    show_figure=False,
)

# Combine Table and Scatterplot via grid layout:
pandas_bokeh.plot_grid([[data_table, p_scatter]],
                       plot_width=400, plot_height=350)
