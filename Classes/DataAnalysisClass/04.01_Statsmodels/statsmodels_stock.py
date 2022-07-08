import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

stock_data = pd.read_csv('SP500.csv', index_col='Date', parse_dates=True)
stock_data = stock_data.sort_index()
