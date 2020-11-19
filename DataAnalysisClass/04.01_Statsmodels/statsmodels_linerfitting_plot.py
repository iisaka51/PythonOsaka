import matplotlib.pyplot as plt

xp = results.predict(exog)

fig, ax = plt.subplots()
ax.plot(data['x'].values, data['y'].values, 'o', label="Data")
ax.plot(data['x'].values, xp.values,'r', label='WLS')
ax.legend(loc="best");
