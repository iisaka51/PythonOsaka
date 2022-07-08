import numpy as np
import pandas as pd
from prettypandas import PrettyPandas

teams_list = ["Dallas", "Chicago", "Los Angelos"]
data = np.array([[1, 2, 1],
                 [0, 1, 0],
                 [2, 4, 1]])

df = pd.DataFrame(data, 'index', teams_list)
print(
    df
      .pipe(PrettyPandas)
      .total(axis=1)
      .average(axis=1)
)
