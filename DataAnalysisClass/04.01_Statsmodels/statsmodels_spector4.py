model = sm.OLS(df[objVar], df[expVar])
result = model.fit()
result.summary()
