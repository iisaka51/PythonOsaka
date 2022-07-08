import numpy as np

a = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12]])

row1 = a[1, :]
row2 = a[1:2, :]

col1 = a[:, 1]
col2 = a[:, 1:2]

rank_a = np.linalg.matrix_rank(a)
rank_row1 = np.linalg.matrix_rank(row1)
rank_row2 = np.linalg.matrix_rank(row2)
rank_col1 = np.linalg.matrix_rank(col1)
rank_col2 = np.linalg.matrix_rank(col2)

print(row1, row1.shape, rank_row1)
print(row2, row2.shape, rank_row2)

print(col1, col1.shape, rank_col1)
print(col2, col2.shape, rank_col2)
                             #          [ 6]
