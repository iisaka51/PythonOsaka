import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from pytrends.request import TrendReq
import seaborn

seaborn.set_style("darkgrid")

pt = TrendReq(hl='en-US', tz=360)

kw_list = ["Python"]
pt.build_payload(kw_list, timeframe="all")

data = pt.related_topics()

# type(data)
# data['Python']['top']
