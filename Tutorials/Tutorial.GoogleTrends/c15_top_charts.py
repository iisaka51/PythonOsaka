import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from pytrends.request import TrendReq
import seaborn

seaborn.set_style("darkgrid")

pt = TrendReq(hl='en-US', tz=360)
data = pt.top_charts(2021,geo='JP')

# data[:10]
