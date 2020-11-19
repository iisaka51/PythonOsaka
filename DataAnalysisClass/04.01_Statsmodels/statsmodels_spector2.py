df = spector.exog
df['result'] = spector.endog
df['intercept'] = 1
df.head().T
