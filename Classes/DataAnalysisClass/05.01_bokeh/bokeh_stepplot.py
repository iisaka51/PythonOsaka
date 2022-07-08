import numpy as np
import pandas as pd
import pandas_bokeh


x = np.arange(-3, 3, 1)
y2 = x**2
y3 = x**3
df = pd.DataFrame({"x": x, "Parabula": y2, "Cube": y3})
df.plot_bokeh.step(
    x="x",
    xticks=range(-1, 1),
    colormap=["#009933", "#ff3399"],
    title="Stepplot (Parabula vs. Cube)",
    figsize=(800,300)
    )

df.plot_bokeh.step(
    x="x",
    xticks=range(-1, 1),
    colormap=["#009933", "#ff3399"],
    title="Stepplot (Parabula vs. Cube)",
    mode="after",
    figsize=(800,300)
    )
