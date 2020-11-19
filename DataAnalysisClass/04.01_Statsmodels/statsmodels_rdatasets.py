import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
guerry = sm.datasets.get_rdataset("Guerry", "HistData").data
results = smf.ols('Lottery ~ Literacy + np.log(Pop1831)',
                  data=guerry).fit()
results.summary()
