import numpy as np
from tabulate import tabulate

data = np.array([["Dallas", "Chicago", "Los Angelos"],
                 [1, 2, 1],
                 [0, 1, 0],
                 [2, 4, 1]])


table = tabulate(data, headers='firstrow', showindex='always')
print(table)
