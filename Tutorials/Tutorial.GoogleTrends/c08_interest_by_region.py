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

# data
# data.filter(items=['Japan', 'United States'], axis='index')
