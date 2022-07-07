from autoviz.AutoViz_Class import AutoViz_Class

AV = AutoViz_Class()

filename = "titanic.csv"
sep = ","

dft = AV.AutoViz(
    filename,
    sep=",",
    depVar="",
    dfte=None,
    header=0,
    verbose=0,
    lowess=False,
    chart_format="bokeh",
    max_rows_analyzed=150000,
    max_cols_analyzed=30,
    save_plot_dir=None
)
