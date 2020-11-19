import numpy as np
import pandas as pd

ser = pd.Series(np.random.randn(8))
df = pd.DataFrame(np.random.randn(10, 4))

print(ser)
# ser.pct_change()
print(df)
