import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from pytrends.request import TrendReq
import seaborn

seaborn.set_style("darkgrid")

pt = TrendReq(hl='en-US', tz=360)

kw_list = ["Python", "Java"]
pt.build_payload(kw_list, timeframe="all")

data = pt.get_historical_interest( kw_list,
             year_start=2022, month_start=2, day_start=1, hour_start=0,
             year_end=2022, month_end=2, day_end=28, hour_end=23,
         )

# %matplotlib
# data.plot(figsize=(10,6))
