import numpy as np

data = [[11,12,13],
        [21,22,23],
        [31,32,33]]

np.savetxt('sample.csv',
           X=data,          # 保存したい配列
           delimiter=","    # 区切り文字
)
