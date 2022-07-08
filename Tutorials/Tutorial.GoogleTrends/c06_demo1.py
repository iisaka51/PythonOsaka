from pytrends.request import TrendReq
import seaborn

seaborn.set_style("darkgrid")

pt = TrendReq(hl='en-US', tz=360)

kw_list = ["Python", "Java"]
pt.build_payload(kw_list, timeframe="all")

iot = pt.interest_over_time()

# %matplotlib
iot.plot(figsize=(10,6))
