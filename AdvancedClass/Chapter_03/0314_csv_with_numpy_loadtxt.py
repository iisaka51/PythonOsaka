import numpy as np

data = np.loadtxt('sample.csv',
                  delimiter=",",    # ファイルの区切り文字
                  skiprows=0,       # 指定した行数をスキップ
                  usecols=(0,1,2)   # 読み込みたい列番号
                 )
print(data)
