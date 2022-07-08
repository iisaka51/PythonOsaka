import numpy as np
import pandas as pd

df = pd.DataFrame(np.random.randn(2, 2))
print(df.head())
print(df.to_html())
