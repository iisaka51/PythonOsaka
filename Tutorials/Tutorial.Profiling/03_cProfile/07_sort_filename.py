import pstats
from pstats import SortKey

p = pstats.Stats('re_test.log')
t1 = p.sort_stats(SortKey.FILENAME).print_stats('__init__')
