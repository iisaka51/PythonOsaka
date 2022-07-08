import numpy as np
from tabulate import tabulate

teams_list = ["Dallas", "Chicago", "Los Angelos"]
data = np.array([[1, 2, 1],
                 [None, 1, None],
                 [2, 4, 1]])


table = tabulate(data, headers=teams_list,
                 missingval='N/A',
                )
print(table)
