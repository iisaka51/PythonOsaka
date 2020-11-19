olsmod = sm.OLS(y, X)
olsres = olsmod.fit()
print(olsres.summary())
