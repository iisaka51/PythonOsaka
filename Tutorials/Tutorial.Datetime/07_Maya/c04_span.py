import maya

dt = maya.when('May 24 2020 08:20:00 JST')

d1 = dt.snap('@d+6h').rfc2822()
d2 = dt.snap('@d+5d+4h+3m+2s').rfc2822()
