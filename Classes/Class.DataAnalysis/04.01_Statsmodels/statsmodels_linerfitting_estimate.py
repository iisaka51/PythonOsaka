exog = sm.add_constant(data['x'])
endog = data['y']
weights = 1. / (data['y_err'] ** 2)
wls = sm.WLS(endog, exog, weights)
results = wls.fit(cov_type='fixed scale')
print(results.summary())
