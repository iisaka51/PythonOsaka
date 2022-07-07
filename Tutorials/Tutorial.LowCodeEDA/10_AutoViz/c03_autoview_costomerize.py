from autoviz.AutoViz_Class import AutoViz_Class
from dataset import load_dataset

df = load_dataset('titanic.csv')

AV = AutoViz_Class()

dft = AV.AutoViz(
    filename="",
    sep=",",
    depVar="",
    dfte=df,
    header=0,
    verbose=0,
    lowess=False,
    chart_format="bokeh",
    max_rows_analyzed=150000,
    max_cols_analyzed=30,
    save_plot_dir=None
)
