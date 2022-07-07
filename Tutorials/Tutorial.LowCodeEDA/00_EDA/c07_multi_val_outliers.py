import random
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame(data={'A': random.sample(range(60, 100), 10),
                        'B': random.sample(range(20, 40), 10),
                        'C': random.sample(range(2000, 3010), 10),
                        'type': list(3*'A')+list(3*'B')+list(4*'C')})

fig, axes = plt.subplots(2,2)

for i,el in enumerate(list(df.columns.values)[:-1]):
    a = df.boxplot(el, by="type", ax=axes.flatten()[i])

fig.delaxes(axes[1,1])
plt.tight_layout()

plt.show()
