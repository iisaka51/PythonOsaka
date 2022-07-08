import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from pytrends.request import TrendReq
import seaborn

seaborn.set_style("darkgrid")

pt = TrendReq(hl='en-US', tz=360)

kw_list = ["Python", "Java"]
pt.build_payload(kw_list, timeframe="all")

data = pt.interest_by_region( "COUNTRY",
         inc_low_vol=False, inc_geo_code=True
         )

# data[kw_list].sort_values('Python', ascending=False).head(10)

# %matplotlib
# data[kw_list].sort_values('Python', ascending=False).head(10).plot.bar()

# data[kw_list].sort_values('Java', ascending=False).head(10)
