# %matplotlib
import pandas as pd
from matplotlib import pyplot as plt
from palmerpenguins import load_penguins

df = load_penguins()

df.describe()

df.hist(figsize=(15,15))
# 9個以上の変数がある場合は、figsizeを大きく設定
plt.tight_layout()
plt.show()
