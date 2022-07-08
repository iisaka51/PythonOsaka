import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.iolib.summary import summary

dat = sm.datasets.get_rdataset("Guerry", "HistData").data
results = smf.ols('Lottery ~ Literacy + np.log(Pop1831)', data=dat).fit()

summary.as_latex(results.summary())
# summary.as_latex
# summary.as_text
# summary.as_csv
# summary.as_html
